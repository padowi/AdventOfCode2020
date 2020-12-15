#!/usr/bin/env python3

"""Advent of Code"""

import os.path
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0]))))
import toolbox as tb

from pprint import pprint


def find_last_occurrence_or_add(x, seq):
    # damnit... the way I am structuring runner below,
    # I'll never get to use this fancy function... :'(
    # I wrote it as a tracer before I had read the full requiremens...
    # so now instead of this, I'll just build some other function
    # that will make more sense for the task, but I like the ugliness
    # of this function so very much that even though it is dead code
    # I'll leave it in here.
    for i in range(1, len(seq) + 1):
        try:
            idx = seq.index(x, i * -1)
            if True: # what a nasty piece of ugly-hack you are, I love it!
                break
        except ValueError:
            continue
    else: # woho, finally got to use for/else!!!
        seq.append(x)
        idx = len(seq)

    return (seq, idx)


def diff_last_two_occurrences_of(x, seq):
    indices = list()
    for (idx, num) in enumerate(seq):
        if num == x:
            indices.append(idx)

    return indices[-1] - indices[-2]


def runner(data, target):
    # ok, so we will either be adding a new number (x not in spoken), or
    # figuring out when number was last seen spoken.?rindex?(x)
    # damnit... lists don't have an rindex() or rfind() or any such thing...
    # strings... on the other hand, has rindex()
    # but I can just build my own :D

    # from the testdata and our input, it seems like the starting numbers
    # are unique, so we don't need to apply rule-checking on them, and
    # could just chuck them all into the list
    # and since they're already in a list... well, I guess we're done
    # with the starting phase :D

    while not len(data) == target:
        lastNumber = data[-1]
        if data.count(lastNumber) == 1:
            data.append(0)
            continue

        # lastNumber can't occur 0 times, since we grabbed it off the back of
        # the list just moments ago,
        # and if we got here, there wasn't 1 singular occurrence either (since
        # we'd have short-circuited out by now if so, which means that there
        # are two or more occurrences of the number in the list.
        data.append(diff_last_two_occurrences_of(lastNumber, data))

    return data[-1]



def main(data):
    """Main program"""
    data = [int(x) for x in data[0].split(',')]
    return runner(data, 2020)


if __name__ == '__main__':
    testVectors = [
        {
            'expectedOutcome': 436,
            'testInput': {
                'data': [0, 3, 6],
                'target': 2020,
            },
            'function': runner,
        },
        {
            'expectedOutcome': 1,
            'testInput': {
                'data': [1, 3, 2],
                'target': 2020,
            },
            'function': runner,
        },
        {
            'expectedOutcome': 10,
            'testInput': {
                'data': [2, 1, 3],
                'target': 2020,
            },
            'function': runner,
        },
        {
            'expectedOutcome': 27,
            'testInput': {
                'data': [1, 2, 3],
                'target': 2020,
            },
            'function': runner,
        },
        {
            'expectedOutcome': 78,
            'testInput': {
                'data': [2, 3, 1],
                'target': 2020,
            },
            'function': runner,
        },
        {
            'expectedOutcome': 438,
            'testInput': {
                'data': [3, 2, 1],
                'target': 2020,
            },
            'function': runner,
        },
        {
            'expectedOutcome': 1836,
            'testInput': {
                'data': [3, 1, 2],
                'target': 2020,
            },
            'function': runner,
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
