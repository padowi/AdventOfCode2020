#!/usr/bin/env python3

"""Advent of Code"""

import os.path
import sys

from math import prod
from pprint import pprint


def calculateString(expression):
    terms = expression.split(' ')
    result = None
    action = term2 = None
    while len(terms):
        if not result:
            result = int(terms.pop(0))
            continue
        elif not action:
            action = terms.pop(0)
            continue
        else:
            term2 = int(terms.pop(0))

        if action == '+':
            result += term2
        elif action == '*':
            result *= term2

        action = term2 = None

    return result


def runner(line, debug=False):
    while "(" in line:
        rightMostParenPos = line.rfind("(")
        matchingEndParen = line.find(")", rightMostParenPos)
        line = line[0:rightMostParenPos] + str(calculateString(line[rightMostParenPos+1:matchingEndParen])) + line[matchingEndParen+1:]

    return calculateString(line)


def main(data):
    """Main program"""
    return sum([runner(line) for line in data])


if __name__ == '__main__':
    testVectors = [
        {
            'expectedOutcome': 71,
            'testInput': {
                'line': "1 + 2 * 3 + 4 * 5 + 6",
                'debug': True,
            },
            'function': runner,
        },
        {
            'expectedOutcome': 51,
            'testInput': {
                'line': "1 + (2 * 3) + (4 * (5 + 6))",
                'debug': True,
            },
            'function': runner,
        },
        {
            'expectedOutcome': 26,
            'testInput': {
                'line': "2 * 3 + (4 * 5)",
                'debug': True,
            },
            'function': runner,
        },
        {
            'expectedOutcome': 437,
            'testInput': {
                'line': "5 + (8 * 3 + 9 + 3 * 4 * 3)",
                'debug': True,
            },
            'function': runner,
        },
        {
            'expectedOutcome': 12240,
            'testInput': {
                'line': "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))",
                'debug': True,
            },
            'function': runner,
        },
        {
            'expectedOutcome': 13632,
            'testInput': {
                'line': "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2",
                'debug': True,
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
                inputData = [line.strip() for line in fh.readlines()]
            print(main(inputData))
        else:
            print("Input file not found")
    else:
        pprint(testResults)

# vim: set filetype=python set foldmethod=marker
