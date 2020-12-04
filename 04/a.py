#!/usr/bin/env python3

"""Advent of Code"""

import os.path
import sys
from pprint import pprint


class Passport(object):
    def __init__(self):
        self._required_fields = [
            'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'
        ]
        self._attributes = {}
        for field in self._required_fields:
            self._attributes.setdefault(field)
        self._attributes['cid'] = None


    def update(self, key, value):
        self._attributes[key] = value


    def is_valid(self):
        for field in self._required_fields:
            if self._attributes[field] is None:
                return False
        return True


    def __str__(self):
        result = "Passport[{}]"
        if self.is_valid():
            return result.format("VALID")

        missing = list()
        for field in self._required_fields:
            if self._attributes[field] is None:
                missing.append(field)

        return result.format(','.join(missing))

    def __repr__(self):
        return self.__str__()


def runner(data):
    # interesting problem, both whitespace and newlines separate fields in passport,
    # wheras passports themselves are separatet in the input list by blank entries...
    # gonna take a page out of Christoffer's book here and objectify the shit out of this
    passports = list()

    prevLine = separator = ''
    p = Passport()
    for line in data:
        # if we come across a separator line in our data
        # we should have completed a passport, so add it
        # to the list of passports
        #
        # also ensure next iteration will handle things accordingly
        #
        # finally, short-circuit the loop, since this line isn't
        # useful for anything else
        if line == separator:
            passports.append(p)
            prevLine = line
            continue

        # otherwise, if the previous line was a separator,
        # we need to set up a new passport object
        if prevLine == separator:
            p = Passport()

        # now to the meat of the problem, parse the line for key/value pairs
        pairs = line.split(' ')
        for pair in pairs:
            key, value = pair.split(':')
            p.update(key, value)

        prevLine = line

    # dumbass! once we exit the loop, we have a dangling passport object not added to the list!
    passports.append(p)

    return sum([1 for p in passports if p.is_valid()])


def main(data):
    """Main algorithm"""
    return runner(data)


if __name__ == '__main__':
    testVectors = [
        {
            'expectedOutcome': 2,
            'testInput': {
                'data': [
		    'ecl:gry pid:860033327 eyr:2020 hcl:#fffffd',
		    'byr:1937 iyr:2017 cid:147 hgt:183cm',
		    '',
		    'iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884',
		    'hcl:#cfa07d byr:1929',
		    '',
		    'hcl:#ae17e1 iyr:2013',
		    'eyr:2024',
		    'ecl:brn pid:760753108 byr:1931',
		    'hgt:179cm',
		    '',
		    'hcl:#cfa07d eyr:2025 pid:166559648',
		    'iyr:2011 ecl:brn hgt:59in',
                ]
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
