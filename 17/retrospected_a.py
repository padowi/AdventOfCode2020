#!/usr/bin/env python3

"""Advent of Code"""

import os.path
import sys

from pprint import pprint


def bootstrapWorld(data):
    worldState = set()
    z = 0

    for y, line in enumerate(data):
        for x, state in enumerate(line):
            if state == '#':
                worldState.add((x, y, z))

    return worldState


def neighbours(coord):
    result = list()
    x, y, z = coord

    for dx in range(x-1, x+2):
        for dy in range(y-1, y+2):
            for dz in range(z-1, z+2):
                tmpCoord = (dx, dy, dz)
                if  tmpCoord != coord:
                    result.append(tmpCoord)

    return result


def countActiveNeighboursFor(coord, worldState):
    allNeighbours = neighbours(coord)
    activeNeighbourCount = 0

    for neighbour in allNeighbours:
        if neighbour in worldState:
            activeNeighbourCount += 1

    return activeNeighbourCount


def runner(data, cycleCount):
    currentState = bootstrapWorld(data);

    for _ in range(cycleCount):
        newState = currentState.copy()

        coordsToEvaluate = set();
        for coord in currentState:
            coordsToEvaluate.add(coord)
            for neighbourCoord in neighbours(coord):
                coordsToEvaluate.add(neighbourCoord)

        for coord in coordsToEvaluate:
            if coord in currentState:
                activeNeighbourCount = countActiveNeighboursFor(coord, currentState)
                if activeNeighbourCount < 2 or activeNeighbourCount > 3:
                    newState.remove(coord)
            else:
                if countActiveNeighboursFor(coord, currentState) == 3:
                    newState.add(coord)

        currentState = newState

    return len(currentState)


def main(data):
    """Main program"""
    return runner(data, 6)


if __name__ == '__main__':
    testVectors = [
        {
            'expectedOutcome': 112,
            'testInput': {
                'data': [
                    '.#.',
                    '..#',
                    '###',
                ],
                'cycleCount': 6
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
