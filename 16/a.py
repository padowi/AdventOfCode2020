#!/usr/bin/env python3

"""Advent of Code"""

import os.path
import re
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0]))))
import toolbox as tb

from pprint import pprint


P_EXTRACT_NUM_RANGES = re.compile(r'^[^:]+: (?P<fromA>\d+)-(?P<toA>\d+) or (?P<fromB>\d+)-(?P<toB>\d+)$')


def runner(data, debug=False):
    # phase 1, parse rules
    valid_numbers = set()
    while data:
        line = data.pop(0)
        if line == '':
            break

        if match := P_EXTRACT_NUM_RANGES.match(line):
            astart = int(match.groupdict()['fromA'])
            aend = int(match.groupdict()['toA']) + 1
            for n in range(astart, aend): valid_numbers.add(n)

            bstart = int(match.groupdict()['fromB'])
            bend = int(match.groupdict()['toB']) + 1
            for n in range(bstart, bend): valid_numbers.add(n)
        else:
            print("ERROR in extraction of number ranges!")
            sys.exit(1)

    if debug: print(valid_numbers)

    # phase 2, parse our ticket
    while data:
        line = data.pop(0)
        if line == '':
            break
        elif line == 'your ticket:':
            continue

        my_ticket =  tb.ints(line)

    if debug: print(my_ticket)

    # phase 3, parse nearby tickets
    numbers_in_violation = list()

    while data:
        line = data.pop(0)
        if line == '':
            break
        elif line == 'nearby tickets:':
            continue

        nearby_ticket = tb.ints(line)
        if debug: print(nearby_ticket)

        for num in nearby_ticket:
            if num not in valid_numbers:
                numbers_in_violation.append(num)

    return sum(numbers_in_violation)


def main(data):
    """Main program"""
    return runner(data)


if __name__ == '__main__':
    testVectors = [
        {
            'expectedOutcome': 71,
            'testInput': {
                'data': [
                    'class: 1-3 or 5-7',
                    'row: 6-11 or 33-44',
                    'seat: 13-40 or 45-50',
                    '',
                    'your ticket:',
                    '7,1,14',
                    '',
                    'nearby tickets:',
                    '7,3,47',
                    '40,4,50',
                    '55,2,20',
                    '38,6,12',
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
