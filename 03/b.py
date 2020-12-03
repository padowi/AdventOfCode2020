#!/usr/bin/env python3

"""Advent of Code"""

import math
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


def tree_checker(data, down, right):
    tree_count = 0
    x = 0

    for y, row in enumerate(data):
        if down > 1:
            if y % down != 0:
                continue
        else:
            x = (y * right) % len(row)

        if row[x] == '#':
            tree_count += 1

        if down > 1:
            x += right
            x = x % len(row)

    return tree_count


def runner(data, slopes):
    slope_results = [tree_checker(data, down, right) for (right, down) in slopes]
    return math.prod(slope_results)


def main(data):
    """Main algorithm"""
    slopes = [ (1, 1), (3, 1), (5, 1), (7, 1), (1, 2) ]
    return runner(data, slopes)


if __name__ == '__main__':
    testVectors = [
        {
            'expectedOutcome': 336,
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
                'slopes': [ # (x, y) (right, down)
                    (1, 1), (3, 1), (5, 1), (7, 1), (1, 2)
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
