#!/usr/bin/env python3

"""Advent of Code"""

import os.path
import sys

from pprint import pprint


def parseInput(data):
    p1 = list()
    p2 = list()

    while data:
        line = data.pop(0)
        if line == 'Player 1:':
            deck = p1
            continue

        if line == '':
            data.pop(0)
            deck = p2
            continue

        deck.append(int(line))

    return (p1, p2)



def runner(data):
    p1, p2 = parseInput(data)

    while len(p1) > 0 and len(p2) > 0:
        c1 = p1.pop(0)
        c2 = p2.pop(0)

        if c1 >= c2:
            p1.append(c1)
            p1.append(c2)
        else:
            p2.append(c2)
            p2.append(c1)

    if len(p1) > len(p2):
        deck = p1
    else:
        deck = p2

    return sum([idx * val for idx, val in enumerate(reversed(deck), start=1)])


def main(data):
    """Main program"""
    return runner(data)


if __name__ == '__main__':
    testVectors = [
        {
            'expectedOutcome': 306,
            'testInput': {
                'data': [
                    'Player 1:', '9', '2', '6', '3', '1',
                    '',
                    'Player 2:', '5', '8', '4', '7', '10',
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
                inputData = [line.strip() for line in fh.readlines()]
            print(main(inputData))
        else:
            print("Input file not found")
    else:
        pprint(testResults)

# vim: set filetype=python set foldmethod=marker
