#!/usr/bin/env python3

"""Advent of Code"""

import os.path
import sys

from copy import deepcopy
from pprint import pprint


# my immediate thought is that we should have a dict, whose keys are (x,y,z)
# tuples.
# the value of this should probably be how amny neighbouring nodes are
# active... no, wait, we also need to have the state of the cube recorded

class Cube(object):
    def __init__(self, coords, state=False):
        self._coords = coords
        self._state = state # True: active, False: inactive


    def neighbours(self):
        x, y, z, w = self._coords
        neighbours = list()
        for dx in range(x-1, x+2):
            for dy in range(y-1, y+2):
                for dz in range(z-1, z+2):
                    for dw in range(w-1, w+2):
                        if (dx, dy, dz, dw) != (x, y, z, w):
                            neighbours.append( (dx, dy, dz, dw) )

        return neighbours


    def is_active(self):
        # True: active
        # False: inactive
        return self._state


    def activate(self):
        self._state = True


    def deactivate(self):
        self._state = False


    def count_active_neighbours(self, world):
        active = 0
        for coord in self.neighbours():
            if coord in world:
                if world[coord].is_active():
                    active += 1

        return active


    def __str__(self):
        return "#"



def populate_world(data):
    world = dict()
    z = 0
    w = 0
    for y, line in enumerate(data):
        for x, state in enumerate(line):
            if state == '#':
                world[(x, y, z, w)] = Cube( (x, y, z, w), True )

    return world


def flat_repr(world):
    minX = minY = minZ = minW = 0
    maxX = maxY = maxZ = maxW = 0

    # determine world boundaries
    for (x, y, z, w) in world.keys():
        if x < minX: minX = x
        elif x > maxX: maxX = x

        if y < minY: minY = y
        elif y > maxY: maxY = y

        if z < minZ: minZ = z
        elif z > maxZ: maxZ = z

        if w < minW: minW = w
        elif w > maxW: maxW = w

    for dw in range(minW, maxW+1):
        for dz in range(minZ, maxZ+1):
            print("z={}, w={}".format(dz, dw))
            for dy in range(minY, maxY+1):
                for dx in range(minX, maxX+1):
                    tmpCoord = (dx, dy, dz, dw)
                    print(world.get(tmpCoord, '.'), end='')
                print('')
            print('')


def count_active_cubes(world):
    active_cube_count = 0
    for coord in world:
        if world[coord].is_active():
            active_cube_count += 1

    return active_cube_count


def runner(data, cycles, debug=False):
    world = populate_world(data)
    if debug: flat_repr(world)

    for i in range(cycles):
        if debug: print("Cycle {}".format(i+1))

        new_world = world.copy()

        coords_to_evaluate = set()
        for coord in world.keys():
            coords_to_evaluate.add(coord)
            for neighbour in world[coord].neighbours():
                coords_to_evaluate.add(neighbour)

        for coord in coords_to_evaluate:
            if coord in world:
                if world[coord].is_active():
                    # 1. an active cube, with at least 2, at most 3 active
                    # neighbours, will remain active, otherwise it will become
                    # inactive
                    num_active_neighbours = world[coord].count_active_neighbours(world)
                    if num_active_neighbours < 2 or num_active_neighbours > 3:
                        del new_world[coord]
                else:
                    # 2. an inactive cube, with exactly 3 active neighbours, will
                    # become active
                    if world[coord].count_active_neighbours(world) == 3:
                        new_world[coord] = Cube(coord, True)

            else:
                # coord was undefined in world, which means that it is an inactive cube,
                # since it is inactive it can't have any influence on activating other cubes
                # so we should be able to safely insert it into the new world as is.
                tmpCube = Cube(coord)
                if tmpCube.count_active_neighbours(world) == 3:
                    new_world[coord] = Cube(coord, True)

        world = new_world

        # if debug: flat_repr(world)
        if debug: print(len(world))
        if debug: input()

    return count_active_cubes(world)


def main(data):
    """Main program"""
    return runner(data, 6)


if __name__ == '__main__':
    testVectors = [
        {
            'expectedOutcome': 848,
            'testInput': {
                'data': [
                    '.#.',
                    '..#',
                    '###',
                ],
                'cycles': 6,
                'debug': True,
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
