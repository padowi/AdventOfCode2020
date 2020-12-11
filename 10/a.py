#!/usr/bin/env python3

"""Advent of Code"""

import os.path
import sys

from pprint import pprint


def runner(data):
    diffCount = { 0: 0, 1: 0, 2: 0, 3: 0 }
    currentJoltOutput = 0

    data.sort()
    devicePlug = max(data) + 3

    while data:
        plug = data.pop(0)
        diff = abs(currentJoltOutput - plug)
        currentJoltOutput += diff
        diffCount[diff] += 1

    diff = abs(currentJoltOutput - devicePlug)
    currentJoltOutput += diff
    diffCount[diff] += 1

    return diffCount[1] * diffCount[3]



def main(data):
    """Main algorithm"""
    return runner(data)


if __name__ == '__main__':
    testVectors = [
        {
            'expectedOutcome': 7 * 5,
            'testInput': {
                'data': [ 16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4, ]
            },
            'function': runner,
        },
        {
            'expectedOutcome': 22 * 10,
            'testInput': {
                'data': [
                    28, 33, 18, 42, 31, 14, 46, 20, 48, 47, 24, 23, 49, 45, 19,
                    38, 39, 11, 1, 32, 25, 35, 8, 17, 7, 9, 4, 2, 34, 10, 3,
                ]
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
