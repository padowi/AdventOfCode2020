#!/usr/bin/env python3

"""Advent of Code"""

import os.path
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0]))))
import toolbox as tb

from pprint import pprint


def turn(currentOrientation, turnDirection, degrees):
    # I cheated and checked the input, there are no half-degrees anywhere, the
    # turn is either 90, 180 or 270

    # this is ugly, but it should get the job done
    if degrees == 270:
        degrees = 90
        if turnDirection == 'L':
            turnDirection = 'R'
        else:
            turnDirection = 'L'

    if degrees == 180:
        if currentOrientation == 'East':
            newOrientation = 'West'
        elif currentOrientation == 'West':
            newOrientation = 'East'
        elif currentOrientation == 'North':
            newOrientation = 'South'
        else:
            newOrientation = 'North'
        return newOrientation

    if turnDirection == 'L':
        if currentOrientation == 'East':
            newOrientation = 'North'
        elif currentOrientation == 'West':
            newOrientation = 'South'
        elif currentOrientation == 'North':
            newOrientation = 'West'
        else:
            newOrientation = 'East'
    else:
        if currentOrientation == 'East':
            newOrientation = 'South'
        elif currentOrientation == 'West':
            newOrientation = 'North'
        elif currentOrientation == 'North':
            newOrientation = 'East'
        else:
            newOrientation = 'West'

    return newOrientation


def move(orientation, pos, action, amount):
    (x, y) = pos
    if action == 'F':
        if orientation == 'North':
            y -= amount
        elif orientation == 'South':
            y += amount
        elif orientation == 'East':
            x += amount
        else:
            x -= amount

        return (x, y)

    if action == 'N':
        y -= amount
    elif action == 'S':
        y += amount
    elif action == 'E':
        x += amount
    else:
        x -= amount

    return (x, y)


def runner(data, orientation):
    pos = (0, 0)

    while data:
        instruction = data.pop(0)
        (action, amount) = instruction[0], int(instruction[1:])

        if action in 'LR':
            orientation = turn(orientation, action, amount)
        else:
            pos = move(orientation, pos, action, amount)

    return tb.manhattan((0,0), pos)


def main(data):
    """Main algorithm"""
    return runner(data, 'East')


if __name__ == '__main__':
    testVectors = [
        {
            'expectedOutcome': 25,
            'testInput': {
                'data': [
                    'F10',
                    'N3',
                    'F7',
                    'R90',
                    'F11',
                ],
                'orientation': 'East'
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
