#!/usr/bin/env python3

"""Advent of Code"""

import os.path
import sys

from collections import deque
from pprint import pprint


def validator(data, testData=False, bufferSize=25):
    numbers = deque(maxlen=bufferSize)
    for _ in range(bufferSize):
        numbers.append(data.pop(0))

    result = list()
    while data:
        num = data.pop(0)
        result.append( is_valid(numbers, num) )
        numbers.append(num)

    return result


def is_valid(data, curNum, testData=False):
    result = list()
    if curNum % 2 == 0:
        # even == additional checks
        for num in data:
            if abs(num - curNum) == int(curNum / 2):
                result.append(False)
            elif abs(num - curNum) in data:
                result.append(True)
    else:
        for num in data:
            result.append(abs(num - curNum) in data)

    return any(result)


def runner(data, testData=False):
    numbers = deque(maxlen=25)
    for _ in range(25):
        numbers.append(data.pop(0))

    while data:
        num = data.pop(0)
        if not is_valid(numbers, num):
            return num

        numbers.append(num)

    return 'NUMBER_NOT_FOUND'


def main(data):
    """Main algorithm"""
    return runner(data)


if __name__ == '__main__':
    testVectors = [
        {
            'expectedOutcome': True,
            'testInput': {
                'data': deque(range(1,26), maxlen=25),
                'curNum': 26,
                'testData': True,
            },
            'function': is_valid,
        },
        {
            'expectedOutcome': True,
            'testInput': {
                'data': deque(range(1,26), maxlen=25),
                'curNum': 49,
                'testData': True,
            },
            'function': is_valid,
        },
        {
            'expectedOutcome': False,
            'testInput': {
                'data': deque(range(1,26), maxlen=25),
                'curNum': 100,
                'testData': True,
            },
            'function': is_valid,
        },
        {
            'expectedOutcome': False,
            'testInput': {
                'data': deque(range(1,26), maxlen=25),
                'curNum': 50,
                'testData': True,
            },
            'function': is_valid,
        },
        {
            'expectedOutcome': [
                True, True, True, True, True, True, True, True, True, False,
                True, True, True, True, True
            ],
            'testInput': {
                'data': [
                    35, 20, 15, 25, 47, 40, 62, 55, 65, 95, 102, 117, 150, 182,
                    127, 219, 299, 277, 309, 576,
                ],
                'testData': True,
                'bufferSize': 5
            },
            'function': validator,
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
