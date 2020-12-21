#!/usr/bin/env python3

"""Advent of Code"""

import os.path
import sys

from pprint import pprint


def parseRules(data):
    rules = dict()
    for rule in data:
        idx, value = rule.split(': ')
        idx = int(idx)
        if '"' in value:
            rules[idx] = value.strip('"')
        else:
            terms = list()
            if ' | ' in value:
                for term in value.split(' | '):
                    terms.append(tuple([int(c) for c in term.split(' ')]))
            else:
                terms.append(tuple([int(c) for c in value.split(' ')]))

            rules[idx] = terms

    return rules


def ruleToStrings(rules, idx, debug=False):
    state = ('', [idx])
    investigate = [ state ]
    completed = set()
    string_count = 0

    while investigate:
        (string, indices) = investigate.pop(0)
        indices = list(indices)

        while indices:
            idx = indices.pop(0)

            if type(rules[idx]) != list:
                string += rules[idx]
                continue

            if len(rules[idx]) == 1:
                for otherIndex in reversed(rules[idx][0]):
                    indices.insert(0, otherIndex)
            else:
                # here is where it gets interesting
                # we are gonna branch here.
                # on the one hand, we are going to continue down a path
                # but at the same time, we need to record our current state,
                # along with the indices we didn't follow

                # actually, this seems wrong, what if we have more indices to
                # process? those should be counted too, right?
                sideTrackIndices = list(rules[idx][1])
                sideTrackIndices.extend(indices)
                investigate.append( (string, sideTrackIndices ) )

                for otherIndex in reversed(rules[idx][0]):
                    indices.insert(0, otherIndex)

        # once we have no more indices to follow, this string is complete
        completed.add(string)

    # once we have nothing more to investigate, we are done
    return sorted(completed)


def parseInput(data):
    rule_lines = list()
    messages = list()

    while data:
        line = data.pop(0)
        if line == '':
            break
        rule_lines.append(line)

    while data:
        line = data.pop(0)
        messages.append(line)

    rules = parseRules(rule_lines)

    return (rules, messages)


def runner(data):
    rules, messages = parseInput(data)
    valid_messages = list()

    rule_strings = ruleToStrings(rules, 0, True)

    for msg in messages:
        if msg in rule_strings:
            valid_messages.append(msg)

    return len(valid_messages)


def main(data):
    """Main program"""
    return runner(data)


if __name__ == '__main__':
    testVectors = [
        {
            'expectedOutcome': sorted(['aab', 'aba']),
            'testInput': {
                'rules': {
                    0: [(1, 2,),],
                    1: 'a',
                    2: [(1, 3,), (3, 1,),],
                    3: 'b',
                },
                'idx': 0,

            },
            'function': ruleToStrings,
        },
        {
            'expectedOutcome': sorted([
                'aaaabb', 'aaabab', 'abbabb', 'abbbab',
                'aabaab', 'aabbbb', 'abaaab', 'ababbb',
            ]),
            'testInput': {
                'rules': {
                    0: [(4, 1, 5)],
                    1: [(2, 3), (3, 2)],
                    2: [(4, 4), (5, 5)],
                    3: [(4, 5), (5, 4)],
                    4: 'a',
                    5: 'b',
                },
                'idx': 0,

            },
            'function': ruleToStrings,
        },
        {
            'expectedOutcome': sorted(['a']),
            'testInput': {
                'rules': {
                    0: 'a',
                    1: 'a',
                    2: [(1, 3,), (3, 1,),],
                    3: 'b',
                },
                'idx': 0,

            },
            'function': ruleToStrings,
        },
        {
            'expectedOutcome': {
                    0: [(1, 2,),],
                    1: 'a',
                    2: [(1, 3,), (3, 1,),],
                    3: 'b',
                },
            'testInput': {
                'data': [
                    '0: 1 2',
                    '1: "a"',
                    '2: 1 3 | 3 1',
                    '3: "b"',
                ],
            },
            'function': parseRules,
        },
        {
            'expectedOutcome': 2,
            'testInput': {
                'data': [
                    '0: 4 1 5',
                    '1: 2 3 | 3 2',
                    '2: 4 4 | 5 5',
                    '3: 4 5 | 5 4',
                    '4: "a"',
                    '5: "b"',
                    '',
                    'ababbb',
                    'bababa',
                    'abbbab',
                    'aaabbb',
                    'aaaabbb',
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
