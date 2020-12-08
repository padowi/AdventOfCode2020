#!/usr/bin/env python3

"""Advent of Code"""

import os.path
import sys

from pprint import pprint

class LoopDetectionError(Exception):
    def __init__(self, message, args):
        super(LoopDetectionError, self).__init__(message)
        self.args = args


class ReadyToBootError(Exception):
    def __init__(self, message, args):
        super(ReadyToBootError, self).__init__(message)
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
        try:
            (instruction, argument) = self._instructions[self._pointer].split(' ')
        except IndexError:
            raise ReadyToBootError("This ain't an error!", args=(self._accumulator,))
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
            raise LoopDetectionError("Loop Detected!", args=(self._previousPointerPositions,))


def runner(data, testData=False):
    # OK, so the problem this time is that we need to modify the instruction
    # set, in a controlled way, and re-run the computer with the modified
    # instruction set continuing to alter a single instruction at a time, as
    # long as we get the LoopDetectionError, and not the ReadyToBootError There
    # is probably some really sneaky way to do this which ain't bruteforce,
    # like checking how close to the end of the instruction set the pointer
    # is...
    # How about this? We let the unaltered instruction set run once. It will
    # lead to a loop. Instead of outputting what the accumulator was at that
    # point, we output the previousPointerPositions
    # Then, outside the program, in runner, we do some analyzing of which
    # pointers were hit, and out of those, which ones were nops and which where
    # jumps
    # Since we can only change ONE singular instruction, and there shouldn't be
    # too many different instructions, we can just clone the instruction set,
    # and change one of the instructions per clone, and re-run the computer
    # with each individual (altered) clone. All but one of them should again
    # lead to loops, with the single outlier leading to ReadyToBoot
    computer = HGC(data)
    while True:
        try:
            computer.step()
        except LoopDetectionError as e:
            cursorPositions = e.args[0]
            break

    positionsToChange = list()
    for pos in cursorPositions:
        if 'jmp' in data[pos] or 'nop' in data[pos]:
            positionsToChange.append(pos)

    dataClones = dict()

    for i in range(len(positionsToChange)):
        dataClones[i] = data[:]
        if 'jmp' in dataClones[i][positionsToChange[i]]:
            dataClones[i][positionsToChange[i]] = dataClones[i][positionsToChange[i]].replace('jmp', 'nop')
        else:
            dataClones[i][positionsToChange[i]] = dataClones[i][positionsToChange[i]].replace('nop', 'jmp')

    if testData: pprint(dataClones)

    for modifiedData in dataClones.values():
        computer = HGC(modifiedData)
        while True:
            try:
                computer.step()
            except ReadyToBootError as e:
                return e.args[0]
            except LoopDetectionError:
                break


def main(data):
    """Main algorithm"""
    return runner(data)


if __name__ == '__main__':
    testVectors = [
        {
            'expectedOutcome': 8,
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
                ],
                'testData': True
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


