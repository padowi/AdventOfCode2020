#!/usr/bin/env python3

"""Advent of Code"""

import os.path
import re
import sys

from pprint import pprint


PATTERN_EXPLODE_INSTRUCTION = re.compile(r'^mem\[(?P<addr>\d+)\] = (?P<val>\d+)$')


def runner(data):
    # this is going to be a lot of busywork...
    # so we'll probably need to keep a register with the current state of the
    # system
    #
    # then, from the data, grab a mask, (data.pop(0)
    #
    # and all while data[0].startswith('mem') grab those as well the ints need
    # to be converted, first from str to int, then from int to their binary
    # representation
    #
    # I am actually not quite sure about what I am being asked to do here, but
    # will give it a try
    memory = dict()

    while data:
        mask = data.pop(0).split(' = ')[-1]

        while len(data) > 0 and data[0].startswith('mem'):
            instruction = data.pop(0)
            if (match := PATTERN_EXPLODE_INSTRUCTION.match(instruction)):
                address = int(match.groupdict()['addr'])
                value = int(match.groupdict()['val'])
                binary_repr = "{val:036b}".format(val=value)

                result = list()
                for (maskBit, valueBit) in zip(mask, binary_repr):
                    if maskBit == 'X':
                        # if X, allow value through
                        result.append(valueBit)
                    else:
                        # else, force it to the mask value
                        result.append(maskBit)

                memory[address] = ''.join(result)

    return sum([int(v, 2) for v in memory.values()])


def main(data):
    """Main program"""
    return runner(data)


if __name__ == '__main__':
    testVectors = [
        {
            'expectedOutcome': 165,
            'testInput': {
                'data': [
                    'mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X',
                    'mem[8] = 11',
                    'mem[7] = 101',
                    'mem[8] = 0',
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
