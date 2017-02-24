import argparse
import time
import os

from cornelldata import CornellData
from textdata import TextData

def parseArgs():
    parser = argparse.ArgumentParser()

    parser.add_argument('--corpus', type = str, default = 'cornell', help = 'dataset to choose (cornell)')
    parser.add_argument('--save', type = str, default = 'save', help = 'directory to load checkpointed models')
    parser.add_argument('--load', type = str, default = 'save', help = 'directory to store checkpointed models')

    return parser.parse_args()

def main():
    print('Welcome to DeepQA v0.1 !')
    print()


    args = parseArgs()

    textData = TextData(args)

    pass

if __name__ == '__main__':
    main()
