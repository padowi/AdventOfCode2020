#!/usr/bin/env python3

"""Advent of Code"""

import os.path
import sys

from pprint import pprint


def is_empty(data, row, col):
    return data[row][col] == 'L'


def countAdjacentOccupiedSeats(data, row, col):
    numOccupiedSeats = 0
    for y in range(row-1, row+2):
        for x in range(col-1, col+2):
            if y < 0: continue
            if x < 0: continue
            if y >= len(data): continue
            if x >= len(data[y]): continue
            if y == row and x == col: continue

            if data[y][x] == '#':
                numOccupiedSeats += 1

    return numOccupiedSeats


def runner(data):
    data = [list(line) for line in data]
    newData = list()

    while data != newData:
        # eventually the playingfield should stabilize
        # at which point this loop should exit
        for y in range(len(data)):
            newData.append(list())

            for x in range(len(data[y])):
                if data[y][x] == '.':
                    newData[y].append('.')
                    continue

                if data[y][x] == 'L':
                    if countAdjacentOccupiedSeats(data, y, x) == 0:
                        newData[y].append('#')
                        continue
                    else:
                        newData[y].append('L')
                        continue
                elif data[y][x] == '#':
                    if countAdjacentOccupiedSeats(data, y, x) >= 4:
                        newData[y].append('L')
                        continue
                    else:
                        newData[y].append('#')
                        continue

                # we should not really get here like ever...
                print("WTF")
                newData[y].append(data[y][x])

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
            'expectedOutcome': 37,
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
