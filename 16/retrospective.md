# Retrospective #

The problem today was a fun one. 16b was especially fun.

You have your input, which is split into three sections:

1. Ticket Field Names with corresponding rules about what numbers are allowed/valid in that field
2. Our ticket (a collection of numbers separated by commas, on a single line)
3. Other peoples tickets (same setup as our ticket in #2, but many lines)

## 16a ##

The meat of this problem is to find all the invalid tickets (we can assume that our own ticket is indeed valid, so we need only concern ourselves with the tickets of others).
And for a ticket to be valid, every number in this comma-separated list of numbers must be able to fit into at least one field, according to the rules of those fields.

So if we grab the example input from the problem:

    class: 1-3 or 5-7
    row: 6-11 or 33-44
    seat: 13-40 or 45-50

    your ticket:
    7,1,14

    nearby tickets:
    7,3,47
    40,4,50
    55,2,20
    38,6,12

We have three Ticket Field Names with corresponding rules, our ticket, and 4 other tickets.

Valid numbers for _class_ are 1, 2, 3, 5, 6, or 7. Valid numbers for _row_ are 6, 7, 8, 9, 10, 11, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, or 44, etc.

The first of the other tickets does fit, because 7 can go into either class or row, 3 can go into class, and 14 can go into seat.

The second ticket is invalid, because while 40 fits into row, 4 doesn't fit anywhere, and then it doesn't matter that 50 conforms to the seat rule.

Heck, we didn't even need to figure out whether or not the various numbers for a ticket fit into unique fields (consider how in the first of the others tickets, 7 could fit in both class and row.

Had the first ticket, instead of having `7,3,47` had `5,3,47` it would still have been considered valid, *even* though both 5 and 3 can only fit into the same field (class).

Fortunately, we don't care about such things in 16a. We just want to find the offending numbers, those that don't fit anywhere...

Which means that we could just enumerate all the numbers from the rules (i.e. `range(1,3)` (actually `range(1,4)` since Python's range function is exclusive of the end number) + `range(5,7)` + `range(6,11)` + `range(33,44)` + `range(13,40)` + `range(45-50)` and chuck all those into a set.

Yes, a list would work as well, but we'd have duplicates, and while that doesn't matter for such small amounts of data, I sometimes actually do remember to think about performance... (wish I'd done that for 15a as well tho'...)

Then, for every of the other peoples tickets, go through their numbers one by one and check if they are in the set of valid numbers, and if it isn't, record that number in a list.

This time it needs to be a list, because apparently we need to sum up all the invalid numbers, to get the answer to 16a.

Pretty straight-forward.


## 16b ##

And here comes the fun problem. I actually quite enjoyed this. I didn't know how to solve this, and had to reason my way to a solution.

_"My code is ugly, knees weak, something something mom's spaghetti(-code)"_

It doesn't matter that the code is long (actual logic is some 125+ lines and 244+ with the extensive comments I wrote so that I could keep track of just what I was doing). I had fun and I managed to reason myself to a solution.

Like in 16a we need to find all the invalid tickets, because with these and the list of all tickets, we can figure out the list of valid tickets.

The problem to solve here is to attempt to figure out which columns in the tickets, correspond to which ticket fields.

The way I figured how to do this is:

1. grab the number found in column 1 for each valid ticket (including our own)
2. for every ticket field check if the complete list of numbers (generated in #1) adheres to the rules of that field
3. if every number adheres to the rules of a field, record into a mapping, that this field could potentially be for column 1 in the tickets
4. grab the number found in column 2 for each valid ticket (including our own)
5. for every ticket field check if the complete list of numbers (generated in #4) adheres to the rules of that field
6. if every number adheres to the rules of a field, record into a mapping, that this field could potentially be for column 2 in the tickets
7. ... notice how this pattern repeats itself every 3 list items...

Eventually we have evaluated every column in the valid tickets, against every ticket field rule, and mapped ticket field names to a sequence of columns that has been found to only contain numbers that conform with that fields rules.

At this point, I thought to myself: _"Either [Eric](https://adventofcode.com/2020/about) is a complete and utter douchebag (unlikely) and has made this problem really hard, or he is a kind soul, who has thrown us a bone."_

What I was thinking about was this: What happens now, if in our mapping, none of the fields has a single column associated with it? What if, for every field in the mapping, there are at least two columns with all valid numbers from the valid tickets?

We'll have to attempt some shit like a graph-search with backtracking and shit.

Fortunately, Eric is a kind soul, and (well, at least for my input) there was one field where only a single columns worth of numbers adhered to the rules of that field.

Why is that good? Because each field needs to have a column associated with it, and this field needs this particular column. Which means that no other field can correspond to that column.

So it is only the small matter of moving this field out of the way, mark it as done, and from all the other fields, remove that column as a potential candidate.

This ought, if everything checks out and Eric is still kind, create yet anotther instance of a field, where there is now only one potential column for which all the numbers match. Mark that field as done, and remove this other column from all the remaining fields lists of potential columns.

Rinse and repeat until all fields are marked done, at which point each field should have a single unique column index associated with it.

Then just grab all the fields where the names begin with "departure", take the column values from those fields, and from our ticket, extract the values found in these identified columns.

Multiply those extracted values togheter, you have your answer, call it a day, proper good job mate!

Why was this so fun? Because it gave me a small window of insight into constraint resolution. I'm sure we did something similar in the AI course back at university in 2006, but I can't really say that I remember all that much from that course, so at worst this was a refresher, and at best it was all new and exciting stuff to me (well, it was new and exciting to me, either way).
