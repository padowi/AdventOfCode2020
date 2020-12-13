#!/usr/bin/env python3

"""Advent of Code"""

import os.path
import sys

from pprint import pprint


def runner(data):
    initialTS = ts = int(data.pop(0))
    buses = [
        int(bus)
        for bus
        in data.pop(0).split(',')
        if bus != 'x'
    ]

    endLoop = False
    while not endLoop:
        for bus in buses:
            if (ts % bus) == 0:
                endLoop = True
                break
        if not endLoop:
            ts += 1

    return bus * (ts - initialTS)


def main(data):
    """Main algorithm"""
    return runner(data)


if __name__ == '__main__':
    testVectors = [
        {
            'expectedOutcome': 295,
            'testInput': {
                'data': [
                    '939',
                    '7,13,x,x,59,x,31,19',
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
