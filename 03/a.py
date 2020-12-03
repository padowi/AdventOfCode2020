#!/usr/bin/env python3

"""Advent of Code"""

import os.path
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0]))))
import toolbox as tb

from collections import defaultdict, deque
from itertools import cycle
from pprint import pprint

# tb.ints(str)
# tb.minmax(1, 2)
# tb.manhattan((x1,y1), (x2,y2))


def runner(data, down, right):
    tree_count = 0
    for y, row in enumerate(data):
        if row[(y * right) % len(row)] == '#':
            tree_count += 1
    return tree_count


def main(data):
    """Main algorithm"""
    return runner(data, 1, 3)


if __name__ == '__main__':
    testVectors = [
        {
            'expectedOutcome': 7,
            'testInput': {
                'data': [
                    '..##.......',
                    '#...#...#..',
                    '.#....#..#.',
                    '..#.#...#.#',
                    '.#...##..#.',
                    '..#.##.....',
                    '.#.#.#....#',
                    '.#........#',
                    '#.##...#...',
                    '#...##....#',
                    '.#..#...#.#',
                ],
                'down': 1,
                'right': 3,
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
