#!/usr/bin/env python3

"""Advent of Code"""

import os.path
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0]))))
import toolbox as tb

from collections import defaultdict, deque
from pprint import pprint


def runner(data, target, debug=False):
    numbers = defaultdict(lambda: deque(maxlen=2))

    for (idx, num) in enumerate(data, start=1):
        if debug: print("turn {}, number {}".format(idx, num))
        numbers[num].append(idx)

    latest_number = 0 if len(numbers[num]) < 2 else num

    for i in range(idx + 1, target + 1):
        if len(numbers[latest_number]) < 2:
            latest_number = 0
            numbers[latest_number].append(i)
        else:
            latest_number = max(numbers[latest_number]) - min(numbers[latest_number])
            numbers[latest_number].append(i)
        if debug: print("turn {}, number {}".format(i, latest_number))
        if debug: input()

    return latest_number


def main(data):
    """Main program"""
    data = [int(x) for x in data[0].split(',')]
    return runner(data, 30_000_000)


if __name__ == '__main__':
    testVectors = [
        {
            'expectedOutcome': 0,
            'testInput': {
                'data': [0, 3, 6],
                'target': 10,
            },
            'function': runner,
        },
        {
            'expectedOutcome': 436,
            'testInput': {
                'data': [0, 3, 6],
                'target': 2020,
            },
            'function': runner,
        },
        {
            'expectedOutcome': 1,
            'testInput': {
                'data': [1, 3, 2],
                'target': 2020,
            },
            'function': runner,
        },
        {
            'expectedOutcome': 10,
            'testInput': {
                'data': [2, 1, 3],
                'target': 2020,
            },
            'function': runner,
        },
        {
            'expectedOutcome': 27,
            'testInput': {
                'data': [1, 2, 3],
                'target': 2020,
            },
            'function': runner,
        },
        {
            'expectedOutcome': 78,
            'testInput': {
                'data': [2, 3, 1],
                'target': 2020,
            },
            'function': runner,
        },
        {
            'expectedOutcome': 438,
            'testInput': {
                'data': [3, 2, 1],
                'target': 2020,
            },
            'function': runner,
        },
        {
            'expectedOutcome': 1836,
            'testInput': {
                'data': [3, 1, 2],
                'target': 2020,
                },
            'function': runner,
        },
        {
            'expectedOutcome': 175594,
            'testInput': {
                'data': [0, 3, 6],
                'target': 30000000,
            },
            'function': runner,
        },
        {
            'expectedOutcome': 2578,
            'testInput': {
                'data': [1, 3, 2],
                'target': 30000000,
            },
            'function': runner,
        },
        {
            'expectedOutcome': 3544142,
            'testInput': {
                'data': [2, 1, 3],
                'target': 30000000,
            },
            'function': runner,
        },
        {
            'expectedOutcome': 261214,
            'testInput': {
                'data': [1, 2, 3],
                'target': 30000000,
            },
            'function': runner,
        },
        {
            'expectedOutcome': 6895259,
            'testInput': {
                'data': [2, 3, 1],
                'target': 30000000,
            },
            'function': runner,
        },
        {
            'expectedOutcome': 18,
            'testInput': {
                'data': [3, 2, 1],
                'target': 30000000,
            },
            'function': runner,
        },
        {
            'expectedOutcome': 362,
            'testInput': {
                'data': [3, 1, 2],
                'target': 30000000,
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
                inputData = [line.strip() for line in fh.readlines()]
            print(main(inputData))
        else:
            print("Input file not found")
    else:
        pprint(testResults)

# vim: set filetype=python set foldmethod=marker
