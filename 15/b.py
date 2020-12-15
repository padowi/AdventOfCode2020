#!/usr/bin/env python3

"""Advent of Code"""

import os.path
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0]))))
import toolbox as tb

from collections import defaultdict, deque
from pprint import pprint


def runner(data, target, debug=False):
    # update, after spending most of the morning wasting cycles and going
    # nowhere, fast, I am going to have to concede defeat, and rebuild the
    # algorithm.

    # what if, instead of a loooooong list of integers, which will become more
    # and more consuming to check, we create a dictionary, holding a list of at
    # most the latest two indices?
    # we also need to keep track of what the last number was.
    # and then we also need a counter to get us to 30_000_000

    # create a dictionary where the default value is an empty list with a max
    # size of two elements
    numbers = defaultdict(lambda: deque(maxlen=2))

    # iterate over every element in data, return a tuple representing the index
    # of the element, and the element (value)
    for (idx, num) in enumerate(data, start=1):
        # add to the dictionary, using the element as the key, to the correct
        # list, the value of the first index that value was found at
        numbers[num].append(idx)
        if debug: print(num, idx, numbers)

    # the latest mentioned number is also the last number in the input data
    # which also happens to be whatever is left in the num variable
    latest_number = num

    # iterate over the sequence of numbers between len(data) and 30_000_000
    # actually, since range will use the first number (start of range) as
    # inclusive, and second number (target) as exclusive, we need to add 1 in
    # both values
    for i in range(idx + 1, target + 1):
        if debug: print('---'*30)
        if debug: print("beginning new iteration {} with latest_number {}".format(i, latest_number))
        # if the list found in dictionary under key `latest_number` doesn't
        # contain any elements
        if len(numbers[latest_number]) == 1:
            if debug: print("we have not seen {} before, latest_number should be set to 0".format(latest_number))
            # we should set latest_number to 0
            latest_number = 0
            # and add the current index to dictionary[latest_number]
            if debug: print("numbers before:")
            if debug: pprint(numbers)
            numbers[latest_number].append(i)
            if debug: print("numbers after:")
            if debug: pprint(numbers)
        # otherwise
        else:
            # add this index to the deque for this latest number, then...
            if debug: print("numbers before:")
            if debug: pprint(numbers)
            numbers[latest_number].append(i)
            if debug: print("numbers after:")
            if debug: pprint(numbers)
            # we calculate the new latest_number by grabbing the two latest
            # indices (the only two in the deque) and subtracting them
            latest_number = max(numbers[latest_number]) - min(numbers[latest_number])
            print('new latest_number calculated to: {}'.format(latest_number))
        if debug: input()

    return latest_number


def main(data):
    """Main program"""
    data = [int(x) for x in data[0].split(',')]
    return runner(data, 30_000_000)


if __name__ == '__main__':
    testVectors = [
        {
            'expectedOutcome': 436,
            'testInput': {
                'data': [0, 3, 6],
                'target': 2020,
                'debug': True,
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
        # {
            # 'expectedOutcome': 175594,
            # 'testInput': {
                # 'data': [0, 3, 6],
                # 'target': 30000000,
            # },
            # 'function': runner,
        # },
        # {
            # 'expectedOutcome': 2578,
            # 'testInput': {
                # 'data': [1, 3, 2],
                # 'target': 30000000,
            # },
            # 'function': runner,
        # },
        # {
            # 'expectedOutcome': 3544142,
            # 'testInput': {
                # 'data': [2, 1, 3],
                # 'target': 30000000,
            # },
            # 'function': runner,
        # },
        # {
            # 'expectedOutcome': 261214,
            # 'testInput': {
                # 'data': [1, 2, 3],
                # 'target': 30000000,
            # },
            # 'function': runner,
        # },
        # {
            # 'expectedOutcome': 6895259,
            # 'testInput': {
                # 'data': [2, 3, 1],
                # 'target': 30000000,
            # },
            # 'function': runner,
        # },
        # {
            # 'expectedOutcome': 18,
            # 'testInput': {
                # 'data': [3, 2, 1],
                # 'target': 30000000,
            # },
            # 'function': runner,
        # },
        # {
            # 'expectedOutcome': 362,
            # 'testInput': {
                # 'data': [3, 1, 2],
                # 'target': 30000000,
            # },
            # 'function': runner,
        # },
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
