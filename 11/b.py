#!/usr/bin/env python3

"""Advent of Code"""

import os.path
import sys

from pprint import pprint


def is_empty(data, row, col):
    return data[row][col] == 'L'


def countOccupiedSeatsInLineOfSight(data, row, col):
    # this one is trickier... first we need to calculate all the coords to
    # check around us, THEN, if those coords happen to be a "." (open floor) we
    # need to proceed in that direction, checking the next tile beyond it,
    # until we reach either an 'L' or a '#', at which point we can say whether
    # or not to increment the occupied chair count.
    numOccupiedSeats = 0

    deltas = [
        (-1, -1), # NW
        (-1, 0),  # N
        (-1, 1),  # NE
        (0, -1),  # W
        (0, 1),   # E
        (1, -1),  # SW
        (1, 0),   # S
        (1, 1),   # SE
    ]

    for delta in deltas:
        rowChange, colChange = delta
        tmpRow = row + rowChange
        tmpCol = col + colChange
        if tmpRow < 0 or tmpRow > len(data): continue
        if tmpCol < 0 or tmpCol > len(data[0]): continue

        try:
            while data[tmpRow][tmpCol] == '.':
                tmpRow = tmpRow + rowChange
                tmpCol = tmpCol + colChange

                if tmpRow < 0 or tmpRow > len(data): raise IndexError()
                if tmpCol < 0 or tmpCol > len(data[0]): raise IndexError()

            if data[tmpRow][tmpCol] == '#':
                numOccupiedSeats += 1
        except IndexError:
            continue

    return numOccupiedSeats


def evolve(data):
    newData = list()
    for y in range(len(data)):
        newData.append(list())

        for x in range(len(data[y])):
            if data[y][x] == '.':
                newData[y].append('.')
                continue

            if data[y][x] == 'L':
                if countOccupiedSeatsInLineOfSight(data, y, x) == 0:
                    newData[y].append('#')
                    continue
                else:
                    newData[y].append('L')
                    continue
            elif data[y][x] == '#':
                if countOccupiedSeatsInLineOfSight(data, y, x) >= 5:
                    newData[y].append('L')
                    continue
                else:
                    newData[y].append('#')
                    continue

            # we should not really get here like ever...
            print("WTF")
            newData[y].append(data[y][x])

    return newData

def runner(data):
    data = [list(line) for line in data]

    while True:
        newData = evolve(data)
        if data == newData:
            break
        data = newData[:]
        newData = list()

    occupiedSeatCount = 0
    for row in data:
        occupiedSeatCount += row.count('#')

    return occupiedSeatCount


def main(data):
    """Main algorithm"""
    return runner(data)


if __name__ == '__main__':
    testVectors = [
        {
            'expectedOutcome': 26,
            'testInput': {
                'data': [
                    'L.LL.LL.LL',
                    'LLLLLLL.LL',
                    'L.L.L..L..',
                    'LLLL.LL.LL',
                    'L.LL.LL.LL',
                    'L.LLLLL.LL',
                    '..L.L.....',
                    'LLLLLLLLLL',
                    'L.LLLLLL.L',
                    'L.LLLLL.LL',
                ],
            },
            'function': runner,
        },
        {
            'expectedOutcome': 0,
            'testInput': {
                'data': [
                    '.##.##.',
                    '#.#.#.#',
                    '##...##',
                    '...L...',
                    '##...##',
                    '#.#.#.#',
                    '.##.##.',
                ],
                'row': 3,
                'col': 3,
            },
            'function': countOccupiedSeatsInLineOfSight,
        },
        {
            'expectedOutcome': 0,
            'testInput': {
                'data': [
                    '.............',
                    '.L.L.#.#.#.#.',
                    '.............',
                ],
                'row': 1,
                'col': 1,
            },
            'function': countOccupiedSeatsInLineOfSight,
        },
        {
            'expectedOutcome': 1,
            'testInput': {
                'data': [
                    '.............',
                    '.L.L.#.#.#.#.',
                    '.............',
                ],
                'row': 1,
                'col': 3,
            },
            'function': countOccupiedSeatsInLineOfSight,
        },
        {
            'expectedOutcome': 8,
            'testInput': {
                'data': [
                    '.......#.',
                    '...#.....',
                    '.#.......',
                    '.........',
                    '..#L....#',
                    '....#....',
                    '.........',
                    '#........',
                    '...#.....',
                ],
                'row': 4,
                'col': 3,
            },
            'function': countOccupiedSeatsInLineOfSight,
        },
        {
            'expectedOutcome': [
                list(line)
                for line
                in [
                    '#.LL.LL.L#',
                    '#LLLLLL.LL',
                    'L.L.L..L..',
                    'LLLL.LL.LL',
                    'L.LL.LL.LL',
                    'L.LLLLL.LL',
                    '..L.L.....',
                    'LLLLLLLLL#',
                    '#.LLLLLL.L',
                    '#.LLLLL.L#',
                ]
            ],
            'testInput': {
                'data': [
                    '#.##.##.##',
                    '#######.##',
                    '#.#.#..#..',
                    '####.##.##',
                    '#.##.##.##',
                    '#.#####.##',
                    '..#.#.....',
                    '##########',
                    '#.######.#',
                    '#.#####.##',
                ],
            },
            'function': evolve,
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
