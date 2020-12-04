#!/usr/bin/env python3

"""Advent of Code"""

import os.path
import sys
import re

from pprint import pprint

PATTERN_HEX_COLOR = re.compile(r'^#([0-9a-f]{6})$')
PATTERN_NINE_DIGITS = re.compile(r'^([0-9]){9}$')

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

        # adding additional validity checks:
        # byr (Birth Year) - four digits; at least 1920 and at most 2002.
        if not 1920 <= int(self._attributes['byr']) <= 2002: return False

        # iyr (Issue Year) - four digits; at least 2010 and at most 2020.
        if not 2010 <= int(self._attributes['iyr']) <= 2020: return False

        # eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
        if not 2020 <= int(self._attributes['eyr']) <= 2030: return False

        # hgt (Height) - a number followed by either cm or in:
        #     If cm, the number must be at least 150 and at most 193.
        #     If in, the number must be at least 59 and at most 76.
        if 'cm' in self._attributes['hgt']:
            at_least = 150
            at_most = 193
        else:
            at_least = 59
            at_most = 76
        if not at_least <= int(self._attributes['hgt'][0:-2]) <= at_most: return False

        # hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
        if not PATTERN_HEX_COLOR.match(self._attributes['hcl']): return False

        # ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
        valid_eye_colors = [ 'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth' ]
        if not self._attributes['ecl'] in valid_eye_colors: return False

        # pid (Passport ID) - a nine-digit number, including leading zeroes.
        if not PATTERN_NINE_DIGITS.match(self._attributes['pid']): return False

        # cid (Country ID) - ignored, missing or not.
        # NOOP

        return True


    def __str__(self):
        result = "Passport[{}]"
        if self.is_valid():
            return result.format("VALID")

        missing = list()
        for field in self._required_fields:
            if self._attributes[field] is None:
                missing.append(field)

        if len(missing) > 0:
            return result.format(','.join(missing))
        else:
            return result.format('INVALID')

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
        {
            'expectedOutcome': 0,
            'testInput': {
                'data': [
                    'eyr:1972 cid:100',
                    'hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926',
                    '',
                    'iyr:2019',
                    'hcl:#602927 eyr:1967 hgt:170cm',
                    'ecl:grn pid:012533040 byr:1946',
                    '',
                    'hcl:dab227 iyr:2012',
                    'ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277',
                    '',
                    'hgt:59cm ecl:zzz',
                    'eyr:2038 hcl:74454a iyr:2023',
                    'pid:3556412378 byr:2007',
                ]
            },
            'function': runner,
        },
        {
            'expectedOutcome': 4,
            'testInput': {
                'data': [
                    'pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980',
                    'hcl:#623a2f',
                    '',
                    'eyr:2029 ecl:blu cid:129 byr:1989',
                    'iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm',
                    '',
                    'hcl:#888785',
                    'hgt:164cm byr:2001 iyr:2015 cid:88',
                    'pid:545766238 ecl:hzl',
                    'eyr:2022',
                    '',
                    'iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719',
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
