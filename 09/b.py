#!/usr/bin/env python3

"""Advent of Code"""

import os.path
import sys

from collections import deque
from pprint import pprint


def runner(data, targetNum, testData=False):
    for idx in range(len(data)):
        for rangeLen in range(idx+1, len(data)):
            rangeSum = sum(data[idx:rangeLen])
            if rangeSum == targetNum:
                return min(data[idx:rangeLen]) + max(data[idx:rangeLen])

            if rangeSum > targetNum:
                break

    return 'NUMBER_NOT_FOUND'


def main(data):
    """Main algorithm"""
    return runner(data, 23278925)


if __name__ == '__main__':
    testVectors = [
        {
            'expectedOutcome': 62,
            'testInput': {
                'data': [
                    35, 20, 15, 25, 47, 40, 62, 55, 65, 95, 102, 117, 150, 182,
                    127, 219, 299, 277, 309, 576,
                ],
                'targetNum': 127,
                'testData': True,
            },
            'function': runner,
        },
        # add more vectors here...
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
