#!/usr/bin/env python3

"""Advent of Code"""

import os.path
import re
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0]))))
import toolbox as tb

from math import prod as product
from pprint import pprint


P_EXTRACT_NUM_RANGES = re.compile(r'^(?P<field>[^:]+): (?P<fromA>\d+)-(?P<toA>\d+) or (?P<fromB>\d+)-(?P<toB>\d+)$')


class TicketField(object):
    def __init__(self, field_name, valid_numbers):
        self._field_name = field_name
        self._valid_numbers = valid_numbers
        self._matching_columns = set()

    def get_valid_numbers(self):
        return self._valid_numbers

    def add_column(self, column):
        self._matching_columns.add(column)

    def count_columns(self):
        return len(self._matching_columns)

    def get_columns(self):
        return self._matching_columns.copy()

    def remove_column(self, column):
        self._matching_columns.remove(column)

    def __str__(self):
        result = "<name: {}, columns: {}>".format(
            self._field_name,
            ', '.join([str(n) for n in self._matching_columns])
        )
        return result

    def __repr__(self):
        return self.__str__()




def runner(data, targetFields, debug=False):
    # phase 1, parse rules

    # we retain the valid_numbers in 16b as well, since it is a quick
    # short-circuit for finding invalid tickets in phase 3
    valid_numbers = set()
    # but we also now need to take the full rules into account, one TicketField
    # object per rule, and those need to be stored somewhere, so let's make a
    # list
    ticket_fields = list()

    while data:
        line = data.pop(0)

        # if we hit a section delimiter,
        if line == '':
            # bug out
            break

        # otherwise extract field name, and valid number ranges
        if match := P_EXTRACT_NUM_RANGES.match(line):
            gd = match.groupdict()
            tmp_numbers = set()

            astart = int(gd['fromA'])
            aend = int(gd['toA']) + 1
            for n in range(astart, aend):
                # a bit ugly adding the same numbers in two places but
                # valid_numbers will eventually grow and contain ANY valid
                # number, whereas tmp_numbers are reset once per iteration and
                # only considers valid numbers for this field
                valid_numbers.add(n)
                tmp_numbers.add(n)

            bstart = int(gd['fromB'])
            bend = int(gd['toB']) + 1
            for n in range(bstart, bend):
                valid_numbers.add(n)
                tmp_numbers.add(n)

            # create a new TicketField object
            ticket_fields.append(TicketField(gd['field'], tmp_numbers))
        else:
            # this shouldn't happen, but them's be famous last words
            print("ERROR in extraction of number ranges!")
            sys.exit(1)


    # phase 2, parse our ticket
    while data:
        line = data.pop(0)
        if line == '':
            break
        elif line == 'your ticket:':
            continue

        my_ticket = tb.ints(line)


    # phase 3, parse nearby tickets

    # we still need to remove all the invalid tickets, so let's create a place
    # to store them, so that we can later check if a ticket is in this list,
    # and if so, not put it in the list of valid tickets
    invalid_tickets = list()

    # any element still in data is either the section heading or a ticket,
    # let's extract the tickets
    all_nearby_tickets = [
        tb.ints(ticket)
        for ticket
        in data
        if not ticket.startswith('nearby')
    ]

    # for each ticket (others tickets)
    for ticket in all_nearby_tickets:
        # consider ever number in the ticket
        for num in ticket:
            # if this number is not a valid number for ANY of the fields
            if num not in valid_numbers:
                # then this ticket simply cannot be valid, regardless of where
                # that number occurred
                invalid_tickets.append(ticket)

    # with the "naughty tickets" list at hand, we can construct a filter which
    # will separate out all the bad tickets from the set of all (other) tickets
    filter_invalid = lambda x: x not in invalid_tickets
    # what we are left with is valid_tickets
    valid_tickets = list(filter(filter_invalid, all_nearby_tickets))
    # however, we should also consider our own ticket as valid, and I am sure
    # it contains some key piece of data to unravel the problem, so we add our
    # ticket to the list of valid tickets as well
    valid_tickets.append(my_ticket)


    # phase 4, match up fields with rules

    # so, now we wish to go through all the ticket fields, one by one, and for each of them,
    # go through every (valid) ticket, column by column, and check whether or
    # not the number in that column (for every ticket) is valid for this
    # TicketField.

    # So it would make sense to create a mapping between column (`idx`) and the
    # values of all tickets in that column
    # (`for ticket in tickets: ticket[idx]`)
    column_value_lookup = dict()

    # we use the length of `my_ticket` since all tickets ought be of equal
    # length, to iterate over the column indices
    for idx in range(len(my_ticket)):
        # and for each index we set up a set in the lookup dictionary (we could
        # have used a list, but what would be the point of potentially storing
        # the same number twice?)
        column_value_lookup[idx] = set()

        # then, for each valid ticket
        for ticket in valid_tickets:
            # grab the value at column index idx, and store in the set at the
            # lookup table on that index
            column_value_lookup[idx].add(ticket[idx])

    # having done that, we can iterate over each ticket_field
    for obj in ticket_fields:
        # and check if all the numbers for a specific column match the rules of
        # that ticket_field, i.e.: for every index
        for key in column_value_lookup:
            # for every number under that index
            for num in column_value_lookup[key]:
                # if number is not valid for this ticket_field,
                if num not in obj.get_valid_numbers():
                    # break loop (we'll continue with another index)
                    break
            else:
                # if we didn't break the loop, all numbers were valid for this
                # ticket_field, add the column index to this TicketField
                obj.add_column(key)

    # now let's set up a record of all the locked-in fields
    done_ticket_fields = list()

    # NOTE: the while loop here could potentially have been an infinite loop,
    # but I made an assumption that the problem would be easy enought that if
    # we had provided the right input data, then one field would only have a
    # single column, and could immediately be locked down, removing that column
    # from all the other fields, which would make another field, contain only
    # one column, this would get picked up in the next iteration, locked in,
    # column removed from all remaining fields, so that another field only had
    # one column, etc etc etc.
    # This assumption turned out to be correct :)

    # while we have fields which have not been locked down
    while ticket_fields:
        # grab the first of those fields
        obj = ticket_fields.pop(0)

        # and if it is not locked down, we can't do anything with it
        if not obj.count_columns() == 1:
            # so add it at the end of the list,
            ticket_fields.append(obj)
            # and begin a new iteration
            continue

        # if we got to this point, our field only has one index
        # (i.e. this column should be locked down to this field)
        # so let's grab the column index
        column_index = obj.get_columns().pop()

        # and then, for every _OTHER_ field in the list
        for obj2 in ticket_fields:
            # let's check if this other field contains the newly/soon to be
            # locked down column index
            if column_index in obj2.get_columns():
                # and if it contains it, it should no longer do that, since our
                # currently worked on field is claiming ownership over it
                # so we remove that column from that field
                obj2.remove_column(column_index)

        # finally, mark this currently worked on field as done (we'll need it
        # later so we cannot just discard it)
        done_ticket_fields.append(obj)

    # having reached this point, all our ticket fields should now have
    # transitioned from ticket_fields to done_ticket_fields, and each only have
    # a single locked in column index each

    # NOTE: we are looking for some specific fields, in our real problem, any
    # field beginning with 'departure', but the way my test framework is set up
    # I need to twist the testdata a little so that I can get a (controlled)
    # passing result, so that my code goes on to the real challenge

    # so let's extract all the fields starting with whatever is in the
    # `targetFields` variable
    ticket_fields = [
        field
        for field
        in done_ticket_fields
        if field._field_name.startswith(targetFields)
    ]

    # from these fields we need to extract their singular locked down column
    columns = [
        obj.get_columns().pop()
        for obj
        in ticket_fields
    ]

    # finally, we'll return to `my_ticket`, and extract all the values from the
    # fields indicated by our extracted columns above, and these values should
    # be multiplied together, to form the answer
    return product( [my_ticket[idx] for idx in columns] )


def main(data):
    """Main program"""
    return runner(data, 'departure')


if __name__ == '__main__':
    testVectors = [
        {
            'expectedOutcome': 12,
            'testInput': {
                'data': [
                    'class: 0-1 or 4-19',
                    'row: 0-5 or 8-19',
                    'seat: 0-13 or 16-19',
                    '',
                    'your ticket:',
                    '11,12,13',
                    '',
                    'nearby tickets:',
                    '3,9,18',
                    '15,1,5',
                    '5,14,9',
                ],
                'targetFields': 'class',
                'debug': True
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
