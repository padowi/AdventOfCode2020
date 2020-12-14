#!/usr/bin/env python3

"""Advent of Code"""

import os.path
import re
import sys

from collections import defaultdict

from pprint import pprint


PATTERN_EXPLODE_INSTRUCTION = re.compile(r'^mem\[(?P<addr>\d+)\] = (?P<val>\d+)$')


def expandAddress(addr):
    targets = [ addr ]
    addresses = list()

    while targets:
        target = targets.pop(0)

        if 'X' in target:
            t1 = t2 = target
            t1 = t1.replace('X', '0', 1)
            targets.append(t1)

            t2 = t2.replace('X', '1', 1)
            targets.append(t2)
        else:
            addresses.append(target)

    return sorted(addresses)



def runner(data):
    # OK, so I am still unsure, because the problem description again isn't
    # terribly well formulated, but I believe, after having read other people's
    # code, that the value of a mem[x] line, should be written into all the
    # memory addresses derived from applying the mask to the value.
    # it seems to me that the other people's code never write to the actual
    # specified address it self at all.

    memory = defaultdict(lambda: "0" * 36)

    while data:
        mask = data.pop(0).split(' = ')[-1]

        while len(data) > 0 and data[0].startswith('mem'):
            instruction = data.pop(0)

            if (match := PATTERN_EXPLODE_INSTRUCTION.match(instruction)):
                address = int(match.groupdict()['addr'])
                value = int(match.groupdict()['val'])
                binVal = "{val:036b}".format(val=value)


                # Immediately before a value is written to memory, each bit in the bitmask modifies the corresponding bit of the destination memory address in the following way:
                # If the bitmask bit is 0, the corresponding memory address bit is unchanged.
                # If the bitmask bit is 1, the corresponding memory address bit is overwritten with 1.
                # If the bitmask bit is X, the corresponding memory address bit is floating.

                binAddr = "{val:036b}".format(val=address)
                resultingAddress = list()

                for (maskBit, addrBit) in zip(mask, binAddr):
                    if maskBit == '0':
                        resultingAddress.append(addrBit)
                    elif maskBit == '1':
                        resultingAddress.append('1')
                    else:
                        resultingAddress.append('X')

                addresses = expandAddress(''.join(resultingAddress))
                for addr in addresses:
                    memory[addr] = binVal

    return sum([int(v, 2) for v in memory.values()])


def main(data):
    """Main program"""
    return runner(data)


if __name__ == '__main__':
    testVectors = [
        {
            'expectedOutcome': sorted(['1100', '1101']),
            'testInput': {
                'addr': '110X'
            },
            'function': expandAddress,
        },
        {
            'expectedOutcome': 208,
            'testInput': {
                'data': [
                    'mask = 000000000000000000000000000000X1001X',
                    'mem[42] = 100',
                    'mask = 00000000000000000000000000000000X0XX',
                    'mem[26] = 1',
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
