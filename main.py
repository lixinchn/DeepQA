import argparse
import time
import os

from cornelldata import CornellData

def parseArgs():
    parser = argparse.ArgumentParser()

    parser.add_argument('--dataset', type = str, default = 'data/cornell', help = 'dataset to choose (cornell)')
    parser.add_argument('--save', type = str, default = 'save', help = 'directory to load checkpointed models')
    parser.add_argument('--load', type = str, default = 'save', help = 'directory to store checkpointed models')

    return parser.parse_args()

def main():
    args = parseArgs()
    cornellData = CornellData('data/cornell')

    pass

if __name__ == '__main__':
    main()
