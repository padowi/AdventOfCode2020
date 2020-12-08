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

class LoopDetectionError(Exception):
    def __init__(self, message, args):
        super(LoopDetectionError, self).__init__(message)
        self.args = args


class HGC(object):
    def __init__(self, instructions):
        self._accumulator = 0
        self._instructions = instructions
        self._pointer = 0
        self._previousPointerPositions = set()


    def acc(self, arg):
        self.debug(self._pointer, 'acc', arg)
        self._accumulator += int(arg)
        self._pointer += 1


    def jmp(self, arg):
        self.debug(self._pointer, 'jmp', arg)
        self._pointer += int(arg)


    def nop(self, arg):
        self.debug(self._pointer, 'nop', arg)
        self._pointer += 1


    def step(self):
        (instruction, argument) = self._instructions[self._pointer].split(' ')
        getattr(self, instruction)(argument)


    def getPointer(self):
        return self._pointer


    def getAccumulator(self):
        return self._accumulator


    def debug(self, pointer, instruction, argument):
        self._previousPointerPositions.add(pointer)
        if instruction == 'jmp':
            newPointerPosition = pointer + int(argument)
        else:
            newPointerPosition = pointer + 1

        if newPointerPosition in self._previousPointerPositions:
            raise LoopDetectionError("Loop Detected!", args=(self._accumulator,))


def runner(data):
    computer = HGC(data)
    while True:
        try:
            computer.step()
        except LoopDetectionError as e:
            return e.args[0]



def main(data):
    """Main algorithm"""
    return runner(data)


if __name__ == '__main__':
    testVectors = [
        {
            'expectedOutcome': 5,
            'testInput': {
                'data': [
                    'nop +0',
                    'acc +1',
                    'jmp +4',
                    'acc +3',
                    'jmp -3',
                    'acc -99',
                    'acc +1',
                    'jmp -4',
                    'acc +6',
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


