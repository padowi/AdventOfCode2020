#!/usr/bin/env python3

"""Advent of Code"""

import os.path
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0])))))
import toolbox as tb
import re

from collections import defaultdict, deque
from itertools import cycle
from pprint import pprint


def verifier(data):
    valid_password_count = 0

    for line in data:
        rule, password = line.split(':')
        password = password.strip()
        positions, char = rule.split(' ')
        first, second = positions.split('-')
        first = int(first) - 1
        second = int(second) - 1
        chars = [ password[first], password[second] ]

        if chars.count(char) == 1:
            valid_password_count += 1

    return valid_password_count


def main(data):
    """Main algorithm"""
    return verifier(data)


if __name__ == '__main__':
    testVectors = [
        {
            'expectedOutcome': 1,
            'testInput': {
                'data': [
                    '1-3 a: abcde',
                    '1-3 b: cdefg',
                    '2-9 c: ccccccccc',
                ]
            },
            'function': verifier,
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
                inputData = [line.strip() for line in fh.readlines()]
            print(main(inputData))
        else:
            print("Input file not found")
    else:
        pprint(testResults)

# vim: set filetype=python set foldmethod=marker
