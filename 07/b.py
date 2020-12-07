#!/usr/bin/env python3

"""Advent of Code"""

import os.path
import re
import sys

from collections import defaultdict
from pprint import pprint


PATTERN_SPLIT_INPUT = re.compile(r'^(?P<container>.*) bags contain (?P<containees>.*)$')
PATTERN_SPLIT_CONTAINEES = re.compile(r'(?P<bag>(?P<amount>\d+) (?P<color>.*?) bags*(?:, |\.))')

def countContainersRecursively(data, testData=False):
    # OK, so in this exercise, we are doing the reverse, i.e. figuring out how
    # many bags we'll be ending up bringing.
    # All of a sudden, the numbers are important, we can no longer use sets,
    # and our fancy datastructure needs to be reversed (i.e. key: container,
    # value: containees)
    # I still think a defaultdict(list) is the appropriate mapping-structure,
    # but this time, the value should probably be a tuple, containing both
    # color and quantity

    relationships = defaultdict(list)

    for line in data:
        if (match := PATTERN_SPLIT_INPUT.match(line)):
            container = match.group('container')
            containees = match.group('containees')

            for bag in PATTERN_SPLIT_CONTAINEES.findall(containees):
                # each match here is a tuple of three elements (because of our
                # three match groups in the pattern)
                # element 0: the full matched string
                # element 1: the amount
                # element 2: the color
                relationships[container].append((int(bag[1]), bag[2]))
            if "no other bags." in containees:
                relationships[container] = None

    if testData: pprint(relationships)

    # Do NOT count the shiny gold bag itself!
    bagCount = 0
    investigate = list()

    investigate.append("shiny gold")
    while investigate:
        lead = investigate.pop(0)
        if relationships[lead]:
            for (amount, color) in relationships[lead]:
                bagCount += amount
                # I can't just add that color once, (dumb-ass), I need to add
                # it as many times as there is amount in the tuple
                for _ in range(amount):
                    investigate.append(color)

    return bagCount


def main(data):
    """Main algorithm"""
    return countContainersRecursively(data)


if __name__ == '__main__':
    testVectors = [
        {
            'expectedOutcome': 32,
            'testInput': {
                'data': [
                    'light red bags contain 1 bright white bag, 2 muted yellow bags.',
                    'dark orange bags contain 3 bright white bags, 4 muted yellow bags.',
                    'bright white bags contain 1 shiny gold bag.',
                    'muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.',
                    'shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.',
                    'dark olive bags contain 3 faded blue bags, 4 dotted black bags.',
                    'vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.',
                    'faded blue bags contain no other bags.',
                    'dotted black bags contain no other bags.',
                ],
                'testData': True
            },
            'function': countContainersRecursively,
        },
        {
            'expectedOutcome': 126,
            'testInput': {
                'data': [
                    'shiny gold bags contain 2 dark red bags.',
                    'dark red bags contain 2 dark orange bags.',
                    'dark orange bags contain 2 dark yellow bags.',
                    'dark yellow bags contain 2 dark green bags.',
                    'dark green bags contain 2 dark blue bags.',
                    'dark blue bags contain 2 dark violet bags.',
                    'dark violet bags contain no other bags.',
                ],
                'testData': True
            },
            'function': countContainersRecursively,
        },
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
