#!/usr/bin/env python3

"""Advent of Code"""

import os.path
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0]))))
import toolbox as tb

from pprint import pprint


def moveWaypoint(shipPos, wpPos, action, amount):
    x, y = wpPos

    if action in 'NSWE':
        if action == 'N':
            y -= amount
        elif action == 'S':
            y += amount
        elif action == 'W':
            x -= amount
        elif action == 'E':
            x += amount
        return (x, y)
    else:
        # ok this isn't going to be fun, nor pretty
        shipX, shipY = shipPos

        if action == 'L':
            # we are going to rotate the coordinates counter-clockwise
            while amount > 0:
                dx = x - shipX
                dy = y - shipY

                x = shipX + dy
                y = shipY + (dx * -1)

                amount -= 90
        else:
            while amount > 0:
                dx = x - shipX
                dy = y - shipY

                x = shipX + (dy * -1)
                y = shipY + dx

                amount -= 90

        return (x, y)


def moveShip(shipPos, wpPos, amount):
    shipX, shipY = shipPos
    wpX, wpY = wpPos

    # calculate where wp is in relationship to ship
    deltaX = wpX - shipX
    deltaY = wpY - shipY

    for _ in range(amount):
        # move ship to WP
        shipPos = wpPos
        # update WP to be in new position relative to ship
        wpPos = ( shipPos[0] + deltaX, shipPos[1] + deltaY )

    return (shipPos, wpPos)


def runner(data, wpPos):
    startPos = shipPos = (0, 0)

    while data:
        instruction = data.pop(0)
        (action, amount) = instruction[0], int(instruction[1:])

        if action == 'F':
            shipPos, wpPos = moveShip(shipPos, wpPos, amount)
        else:
            wpPos = moveWaypoint(shipPos, wpPos, action, amount)

    return tb.manhattan(startPos, shipPos)


def main(data):
    """Main algorithm"""
    return runner(data, (10, -1))


if __name__ == '__main__':
    testVectors = [
        {
            'expectedOutcome': 110,
            'testInput': {
                'data': [ 'F10', ],
                'wpPos': (10, -1)
            },
            'function': runner,
        },
        {
            'expectedOutcome': 110,
            'testInput': {
                'data': [ 'F10', 'N3', ],
                'wpPos': (10, -1)
            },
            'function': runner,
        },
        {
            'expectedOutcome': 208,
            'testInput': {
                'data': [ 'F10', 'N3', 'F7', ],
                'wpPos': (10, -1)
            },
            'function': runner,
        },
        {
            'expectedOutcome': 208,
            'testInput': {
                'data': [ 'F10', 'N3', 'F7', 'R90', ],
                'wpPos': (10, -1)
            },
            'function': runner,
        },
        {
            'expectedOutcome': 286,
            'testInput': {
                'data': [
                    'F10',
                    'N3',
                    'F7',
                    'R90',
                    'F11',
                ],
                'wpPos': (10, -1)
            },
            'function': runner,
        },
        {
            'expectedOutcome': ( (10, -1), (20, -2) ),
            'testInput': {
                'shipPos': (0, 0),
                'wpPos': (10, -1),
                'amount': 1,
            },
            'function': moveShip,
        },
        {
            'expectedOutcome': ( 10, -2 ),
            'testInput': {
                'shipPos': (0, 0),
                'wpPos': (10, -1),
                'action': 'N',
                'amount': 1,
            },
            'function': moveWaypoint,
        },
        {
            'expectedOutcome': ( -1, -10 ),
            'testInput': {
                'shipPos': (0, 0),
                'wpPos': (10, -1),
                'action': 'L',
                'amount': 90,
            },
            'function': moveWaypoint,
        },
        {
            'expectedOutcome': ( 1, 10 ),
            'testInput': {
                'shipPos': (0, 0),
                'wpPos': (10, -1),
                'action': 'R',
                'amount': 90,
            },
            'function': moveWaypoint,
        },
        {
            'expectedOutcome': ( -10, 1 ),
            'testInput': {
                'shipPos': (0, 0),
                'wpPos': (10, -1),
                'action': 'R',
                'amount': 180,
            },
            'function': moveWaypoint,
        },
        {
            'expectedOutcome': ( -10, 1 ),
            'testInput': {
                'shipPos': (0, 0),
                'wpPos': (10, -1),
                'action': 'L',
                'amount': 180,
            },
            'function': moveWaypoint,
        },
        {
            'expectedOutcome': ( -1, -10 ),
            'testInput': {
                'shipPos': (0, 0),
                'wpPos': (10, -1),
                'action': 'R',
                'amount': 270,
            },
            'function': moveWaypoint,
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
