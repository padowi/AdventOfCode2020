#!/usr/bin/env python3

"""Advent of Code"""

import os.path
import sys
import math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0]))))
import toolbox as tb

from collections import defaultdict, deque
from itertools import cycle, combinations
from pprint import pprint


def runner(data, constituents, target=2020):
    for pair in combinations(data, constituents):
        if sum(pair) == target:
            return math.prod(pair)
    return 'NOT_FOUND'


def main(data):
    """Main algorithm"""
    return runner(data, 3, 2020)


if __name__ == '__main__':
    testVectors = [
        {
            'expectedOutcome': 241861950,
            'testInput': {
                'data': [ 1721, 979, 366, 299, 675, 1456 ],
                'constituents': 3,
                'target': 2020,
            },
            'function': runner,
        },
    ]

    testResults = [
        ({
            'index': idx,
            'state': (actualOutcome := tv['function'](**tv['testInput'])) == tv['expectedOutcome'],
            'expected': tv['expectedOutcome'],
            'received': actualOutcome,
        }, print("\aTest {} executed with result {}".format(idx, 'PASS' if actualOutcome == tv['expectedOutcome'] else 'FAIL')))[0]
        for idx, tv
        in enumerate(testVectors)
    ]
    if all([result['state'] for result in testResults]):
        print("All tests passed!")
        inputFile = os.path.join(
            os.path.dirname(
                os.path.abspath(sys.argv[0])
            ), 'input'
        )
        if os.path.isfile(inputFile):
            with open(inputFile, 'r') as fh:
                inputData = [int(line.strip()) for line in fh.readlines()]
            print(main(inputData))
        else:
            print("Input file not found")
    else:
        pprint(testResults)

# vim: set filetype=python set foldmethod=marker
