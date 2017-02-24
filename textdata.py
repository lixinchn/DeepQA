import nltk
from tqdm import tqdm
import pickle
import os

from cornelldata import CornellData

class TextData:
    def __init__(self, args):
        self.corpusDir = 'data/cornell/'
        self.samplesDir = 'data/samples/'
        self.samplesName = 'dataset.pkl'

        self.goToken = -1 # Start of sequence
        self.eosToken = -1 # End of sequence
        self.unknownToken = -1 # Word dropped from vocabulary

        self.trainingSamples = [] # 2d array containing each question and his answer

        self.word2id = {}
        self.id2word = {} # For a rapid conversion

        self.loadCorpus(self.samplesDir)

        pass

    def loadCorpus(self, dirName):
        datasetExist = False
        if os.path.exists(dirName + self.samplesName):
            datasetExist = True

        if not datasetExist: # Fist time we load the database: creating all files
            print('Training samples not found. Creating dataset...')
            # Corpus creation
            cornellData = CornellData(self.corpusDir)
            self.createCorpus(cornellData.getConversations())

            # Saving
            print('Saving dataset...')
            self.saveDataset(dirName) # saving tf samples
        else:
            print('Loading dataset from %s...' % (dirName))
            self.loadDataset(dirName)
            pass

        print('Loaded: %d words, %d QA' % (len(self.word2id), len(self.trainingSamples)))

    def saveDataset(self, dirName):
        with open(dirName + self.samplesName, 'wb') as handle:
            data = {
                "word2id": self.word2id,
                "id2word": self.id2word,
                "trainingSamples": self.trainingSamples
            }
            pickle.dump(data, handle, -1) # Using the highest protocol available

    def loadDataset(self, dirName):
        with open(dirName + self.samplesName, 'rb') as handle:
            data = pickle.load(handle)
            self.word2id = data['word2id']
            self.id2word = data['id2word']
            self.trainingSamples = data['trainingSamples']

            self.goToken = self.word2id['<go>']
            self.eosToken = self.word2id['<eos>']
            self.unknownToken = self.word2id['<unknown>'] # Restore special words

    def createCorpus(self, conversations):
        self.goToken = self.makeWordId('<go>')
        self.eosToken = self.makeWordId('<eos>')
        self.unknownToken = self.makeWordId('<unknown>')

        for conversation in tqdm(conversations, desc = 'Extract conversations'):
            self.extractConversation(conversation)

    def extractConversation(self, conversation):
        for i in range(len(conversation['lines']) - 1): # We ignore the last line
            inputLine = conversation['lines'][i]
            targetLine = conversation['lines'][i + 1]

            inputWords = self.extractText(inputLine['text'])
            targetWords = self.extractText(targetLine['text'], True)

            if not inputWords or not targetWords: # If one of the list is empty
                tqdm.write('Error with some sentences. Sample ignored.')
                if inputWords:
                    tqdm.write(inputLine['text'])
                if targetWords:
                    tqdm.write(targetLine['text'])
            else:
                inputWords.reverse() # Reverse inputs (apparently not the output)

                targetWords.insert(0, self.goToken)
                targetWords.append(self.eosToken) # Add the end of string

                self.trainingSamples.append([inputWords, targetWords])

    def extractText(self, line, isTarget = False):
        words = []

        tokens = nltk.word_tokenize(line)
        for token in tokens:
            words.append(self.makeWordId(token))
        return words

    def makeWordId(self, word):
        id = self.word2id.get(word, -1)

        if id == -1:
            id = len(self.word2id)
            self.word2id[word] = id
            self.id2word[id] = word
        return id

    def playADialog():
        pass
