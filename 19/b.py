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


def validMessage(rules, idx, msg, debug=False):
    state = ('', [idx])
    investigate = [ state ]
    completed = set()
    string_count = 0

    while investigate:
        (string, indices) = investigate.pop(0)
        indices = list(indices)

        if not msg.startswith(string):
            continue

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
    return msg in completed


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
    # 19a was slow as molasses so I am thinking about doing things a little bit
    # different, namely:
    # instead of generating every possible string that the rules could
    # generate, and then comparing them all against the messages,
    # I could iterate over messages one by one, passing it to ruleToStrings
    # (that should probably change name) in which we attempt to build a string
    # and at every branch where we deviate from the message, we quickly abandon
    # that branch altogether.
    # something like
    # if not message.startsWith(stringBeingBuiltWithRules):
    #   bail out of this attempt
    # We'd run ruleToStrings a heck of a lot more times, but hopefully not for
    # as long.
    # On the other hand, it doesn't hurt to attempt bruteforcing it either
    # (although I assume that those two changed rules makes the problem space
    # balloon), so I'll commit here, without the fancy refactor, so that I can
    # run the original code (+ rule changes) on the beefier machine
    #
    # as expected, with the new test cases in place, and the new rules, it is
    # far too slow, we need a new approach
    rules, messages = parseInput(data)
    valid_messages = list()

    for msg in messages:
        if validMessage(rules, 0, msg):
            valid_messages.append(msg)

    return len(valid_messages)


def main(data):
    """Main program"""
    # apparently our data was incorrect in 19a and we need to fix it before
    # passing it on to runner
    data.remove('8: 42')
    data.insert(0, '8: 42 | 42 8')

    data.remove('11: 42 31')
    data.insert(0, '11: 42 31 | 42 11 31')
    return runner(data)


if __name__ == '__main__':
    testVectors = [
	# {
	    # 'expectedOutcome': sorted(['aab', 'aba']),
	    # 'testInput': {
		# 'rules': {
		    # 0: [(1, 2,),],
		    # 1: 'a',
		    # 2: [(1, 3,), (3, 1,),],
		    # 3: 'b',
		# },
		# 'idx': 0,

	    # },
	    # 'function': ruleToStrings,
	# },
	# {
	    # 'expectedOutcome': sorted([
		# 'aaaabb', 'aaabab', 'abbabb', 'abbbab',
		# 'aabaab', 'aabbbb', 'abaaab', 'ababbb',
	    # ]),
	    # 'testInput': {
		# 'rules': {
		    # 0: [(4, 1, 5)],
		    # 1: [(2, 3), (3, 2)],
		    # 2: [(4, 4), (5, 5)],
		    # 3: [(4, 5), (5, 4)],
		    # 4: 'a',
		    # 5: 'b',
		# },
		# 'idx': 0,

	    # },
	    # 'function': ruleToStrings,
	# },
	# {
	    # 'expectedOutcome': sorted(['a']),
	    # 'testInput': {
		# 'rules': {
		    # 0: 'a',
		    # 1: 'a',
		    # 2: [(1, 3,), (3, 1,),],
		    # 3: 'b',
		# },
		# 'idx': 0,

	    # },
	    # 'function': ruleToStrings,
	# },
	# {
	    # 'expectedOutcome': {
		    # 0: [(1, 2,),],
		    # 1: 'a',
		    # 2: [(1, 3,), (3, 1,),],
		    # 3: 'b',
		# },
	    # 'testInput': {
		# 'data': [
		    # '0: 1 2',
		    # '1: "a"',
		    # '2: 1 3 | 3 1',
		    # '3: "b"',
		# ],
	    # },
	    # 'function': parseRules,
	# },
	# {
	    # 'expectedOutcome': 2,
	    # 'testInput': {
		# 'data': [
		    # '0: 4 1 5',
		    # '1: 2 3 | 3 2',
		    # '2: 4 4 | 5 5',
		    # '3: 4 5 | 5 4',
		    # '4: "a"',
		    # '5: "b"',
		    # '',
		    # 'ababbb',
		    # 'bababa',
		    # 'abbbab',
		    # 'aaabbb',
		    # 'aaaabbb',
		# ],
	    # },
	    # 'function': runner,
	# },
        {
            'expectedOutcome': 3,
            'testInput': {
		'data': [
		    '42: 9 14 | 10 1',
		    '9: 14 27 | 1 26',
		    '10: 23 14 | 28 1',
		    '1: "a"',
		    '11: 42 31',
		    '5: 1 14 | 15 1',
		    '19: 14 1 | 14 14',
		    '12: 24 14 | 19 1',
		    '16: 15 1 | 14 14',
		    '31: 14 17 | 1 13',
		    '6: 14 14 | 1 14',
		    '2: 1 24 | 14 4',
		    '0: 8 11',
		    '13: 14 3 | 1 12',
		    '15: 1 | 14',
		    '17: 14 2 | 1 7',
		    '23: 25 1 | 22 14',
		    '28: 16 1',
		    '4: 1 1',
		    '20: 14 14 | 1 15',
		    '3: 5 14 | 16 1',
		    '27: 1 6 | 14 18',
		    '14: "b"',
		    '21: 14 1 | 1 14',
		    '25: 1 1 | 1 14',
		    '22: 14 14',
		    '8: 42',
		    '26: 14 22 | 1 20',
		    '18: 15 15',
		    '7: 14 5 | 1 21',
		    '24: 14 1',
		    '',
		    'abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa',
		    'bbabbbbaabaabba',
		    'babbbbaabbbbbabbbbbbaabaaabaaa',
		    'aaabbbbbbaaaabaababaabababbabaaabbababababaaa',
		    'bbbbbbbaaaabbbbaaabbabaaa',
		    'bbbababbbbaaaaaaaabbababaaababaabab',
		    'ababaaaaaabaaab',
		    'ababaaaaabbbaba',
		    'baabbaaaabbaaaababbaababb',
		    'abbbbabbbbaaaababbbbbbaaaababb',
		    'aaaaabbaabaaaaababaa',
		    'aaaabbaaaabbaaa',
		    'aaaabbaabbaaaaaaabbbabbbaaabbaabaaa',
		    'babaaabbbaaabaababbaabababaaab',
		    'aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba',
		    ],
            },
            'function': runner,
        },
        {
            'expectedOutcome': 12,
            'testInput': {
		'data': [
		    '42: 9 14 | 10 1',
		    '9: 14 27 | 1 26',
		    '10: 23 14 | 28 1',
		    '1: "a"',
		    '11: 42 31 | 42 11 31',
		    '5: 1 14 | 15 1',
		    '19: 14 1 | 14 14',
		    '12: 24 14 | 19 1',
		    '16: 15 1 | 14 14',
		    '31: 14 17 | 1 13',
		    '6: 14 14 | 1 14',
		    '2: 1 24 | 14 4',
		    '0: 8 11',
		    '13: 14 3 | 1 12',
		    '15: 1 | 14',
		    '17: 14 2 | 1 7',
		    '23: 25 1 | 22 14',
		    '28: 16 1',
		    '4: 1 1',
		    '20: 14 14 | 1 15',
		    '3: 5 14 | 16 1',
		    '27: 1 6 | 14 18',
		    '14: "b"',
		    '21: 14 1 | 1 14',
		    '25: 1 1 | 1 14',
		    '22: 14 14',
		    '8: 42 | 42 8',
		    '26: 14 22 | 1 20',
		    '18: 15 15',
		    '7: 14 5 | 1 21',
		    '24: 14 1',
		    '',
		    'abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa',
		    'bbabbbbaabaabba',
		    'babbbbaabbbbbabbbbbbaabaaabaaa',
		    'aaabbbbbbaaaabaababaabababbabaaabbababababaaa',
		    'bbbbbbbaaaabbbbaaabbabaaa',
		    'bbbababbbbaaaaaaaabbababaaababaabab',
		    'ababaaaaaabaaab',
		    'ababaaaaabbbaba',
		    'baabbaaaabbaaaababbaababb',
		    'abbbbabbbbaaaababbbbbbaaaababb',
		    'aaaaabbaabaaaaababaa',
		    'aaaabbaaaabbaaa',
		    'aaaabbaabbaaaaaaabbbabbbaaabbaabaaa',
		    'babaaabbbaaabaababbaabababaaab',
		    'aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba',
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
