#!/usr/bin/env python3

"""Advent of Code"""

import os.path
import sys

from collections import defaultdict
from pprint import pprint

def runner(data):
    groupID = 0
    declarations = defaultdict(dict)
    memberCount = 0

    for line in data:
        if line == '':
            groupID += 1
            declarations[groupID]['memberCount'] = 0
            continue

        declarations[groupID]['memberCount'] = declarations[groupID].get('memberCount', 0) + 1

        for answer in line:
            declarations[groupID][answer] = declarations[groupID].get(answer, 0) + 1

    result = 0
    for groupID in declarations.keys():
        memberCount = declarations[groupID]['memberCount']
        del declarations[groupID]['memberCount']
        for value in declarations[groupID].values():
            if value == memberCount:
                result += 1

    return result


def main(data):
    """Main algorithm"""
    return runner(data)


if __name__ == '__main__':
    testVectors = [
        {
            'expectedOutcome': 6,
            'testInput': {
                'data': [
                    'abc', '',
                    'a', 'b', 'c', '',
                    'ab', 'ac', '',
                    'a', 'a', 'a', 'a', '',
                    'b',
                ],
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
