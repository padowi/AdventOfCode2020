#!/usr/bin/env python3

"""Advent of Code"""

import os.path
import sys

from pprint import pprint

def calculateSeatID(row, col):
    return (row * 8) + col


def boardingPassesToSeats(boardingPasses):
    result = dict()

    for boardingPass in boardingPasses:
        rows = list(range(128))
        cols = list(range(8))

        rowInstructions = boardingPass[0:7]
        colInstructions = boardingPass[7:]

        for ri in rowInstructions:
            if ri == 'F':
                rows = rows[0:int(len(rows)/2)]
            else:
                rows = rows[int(len(rows)/2):]

        row = rows[0]

        for ci in colInstructions:
            if ci == 'L':
                cols = cols[0:int(len(cols)/2)]
            else:
                cols = cols[int(len(cols)/2):]

        col = cols[0]

        result[boardingPass] = (row, col)

    return result


def main(data):
    """Main algorithm"""
    passSeatMapping = boardingPassesToSeats(data)
    seatIDs = [calculateSeatID(row, col) for (row, col) in passSeatMapping.values()]
    return max(seatIDs)


if __name__ == '__main__':
    testVectors = [
        {
            'expectedOutcome': 357,
            'testInput': {
                'row': 44,
                'col': 5,
            },
            'function': calculateSeatID,
        },
        {
            'expectedOutcome': 567,
            'testInput': {
                'row': 70,
                'col': 7,
            },
            'function': calculateSeatID,
        },
        {
            'expectedOutcome': 119,
            'testInput': {
                'row': 14,
                'col': 7,
            },
            'function': calculateSeatID,
        },
        {
            'expectedOutcome': 820,
            'testInput': {
                'row': 102,
                'col': 4,
            },
            'function': calculateSeatID,
        },
        {
            'expectedOutcome': {'FBFBBFFRLR': (44, 5)},
            'testInput': {
                'boardingPasses': ['FBFBBFFRLR'],
            },
            'function': boardingPassesToSeats,
        },
        {
            'expectedOutcome': {'BFFFBBFRRR': (70, 7)},
            'testInput': {
                'boardingPasses': ['BFFFBBFRRR'],
            },
            'function': boardingPassesToSeats,
        },
        {
            'expectedOutcome': {'FFFBBBFRRR': (14, 7)},
            'testInput': {
                'boardingPasses': ['FFFBBBFRRR'],
            },
            'function': boardingPassesToSeats,
        },
        {
            'expectedOutcome': {'BBFFBBFRLL': (102, 4)},
            'testInput': {
                'boardingPasses': ['BBFFBBFRLL'],
            },
            'function': boardingPassesToSeats,
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
