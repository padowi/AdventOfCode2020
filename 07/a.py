#!/usr/bin/env python3

"""Advent of Code"""

import os.path
import re
import sys

from collections import defaultdict
from pprint import pprint


PATTERN_SPLIT_INPUT = re.compile(r'^(?P<container>.*) bags contain (?P<containees>.*)$')
PATTERN_SPLIT_CONTAINEES = re.compile(r'(?P<bag>(?P<amount>\d+) (?P<color>.*?) bags*(?:, |\.))')

def countContainers(data, testData=False):
    # this one will depend so very much on how we chose to represent the rules
    # once we have parsed it.
    # I am thinking that we need a dictionary of lists where the key is the
    # colored bags, and the value is the list of bags in which they go
    # the problem input is all "container" -> "contained"
    # and the dict I wish to build will be
    # "contained" -> "containers"
    # once that is done, we can pick the Shiny Gold bag from the keys, and
    # start creating a set of colors, and for each color in that set add
    # another set of colors where those colors where the key...
    # actually, we need a set (the final account of all colors), and a work
    # list of colors we add, so that we can ignore processing the same color
    # over and over.

    relationships = defaultdict(list)

    colors = set()
    investigate = set()

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
                relationships[bag[2]].append(container)

    if testData: pprint(relationships)

    investigate.add("shiny gold")

    while investigate:
        lead = investigate.pop()
        for color in relationships[lead]:
            colors.add(color)
            investigate.add(color)

    return len(colors)


def main(data):
    """Main algorithm"""
    return countContainers(data)


if __name__ == '__main__':
    testVectors = [
        {
            'expectedOutcome': 4,
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
            'function': countContainers,
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
