#!/usr/bin/env python3

"""Advent of Code"""

import os.path
import sys

from math import prod
from pprint import pprint


def calculateString(expression):
    terms = expression.split(' ')
    pprint(terms)
    while '+' in terms:
        plusLoc = terms.index('+')
        termA = int(terms[plusLoc-1])
        termB = int(terms[plusLoc+1])
        terms.pop(plusLoc+1)
        terms.pop(plusLoc)
        terms[plusLoc-1] = str(termA + termB)

    while '*' in terms:
        prodLoc = terms.index('*')
        terms.pop(prodLoc)

    return prod([int(x) for x in terms])


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
            'expectedOutcome': 231,
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
            'expectedOutcome': 46,
            'testInput': {
                'line': "2 * 3 + (4 * 5)",
                'debug': True,
            },
            'function': runner,
        },
        {
            'expectedOutcome': 1445,
            'testInput': {
                'line': "5 + (8 * 3 + 9 + 3 * 4 * 3)",
                'debug': True,
            },
            'function': runner,
        },
        {
            'expectedOutcome': 669060,
            'testInput': {
                'line': "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))",
                'debug': True,
            },
            'function': runner,
        },
        {
            'expectedOutcome': 23340,
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
