# Retrospective #

On first sight, my mind screamed **AWK**. I actually believe this would be a much simpler solution, than using Python.

But that also means that, while it is good and well to know the strengths of each tool, and when to use them, that I have here an opportunity to learn something new about Python.

For shits and giggles I will probably implement the solution in AWK later on anyway, because why the heck not, but for now, Python it is.

## 4a ##

This problem didn't end up as hairy as I thought it would be. I assumed I would have much trouble with the separation of records (i.e. passports), due to the blank line being the separator, but it didn't turn out to be a great issue.

This time, however, I made a decision which I believe was actually crucial to the above *"empty-lines-separates-passports"* problem not actually being a problem.

A colleague at work usually wants to turn the data into neat representations, essentially objectifying them. He is much better at systemic thinking than me, and his approach leads to more robust, stable, and in the end maintainable solutions.

For Advent of Code type one-off challenges in good fun, this could at times lead to a little bit of over-engineering (the bitcode computer of AoC 2019 was absolutely the right place for systemic thinking and objectification), but say, for the previous three (six) problems of this year, it could be a bit much.

Today was not such a day. Today I objectified. And I believe that made a real difference in how I approached the problem.

I could just as easily have created a list of dictionaries, instead of a list of passport objects (which forced me to first create a passport class), but I am not sure that I would have thought about doing that, at least not until first having gone off one some wild goose chase trying to parse the entries into a list of lists or something equally dumb.

And then there is also the benefit of the passport object that I could write validation logic self-contained in the class, instead of externally and having to apply one or more validation functions on the list of (presumably) dictionaries.

### Attempt #1 ###

    passports = list()
    prevLine = separator = ''
    p = Passport()

    for line in data:
        if line == separator:
            passports.append(p)
            prevLine = line
            continue

        if prevLine == separator:
            p = Passport()

        pairs = line.split(' ')
        for pair in pairs:
            key, value = pair.split(':')
            p.update(key, value)

        prevLine = line

    return sum([1 for p in passports if p.is_valid()])

My first attempt at a solution amounted to this. There is a very subtle error in here, and due to the way the test-data was laid out, the test passed, while the generated answer I submitted turned out to be wrong.

There's a bunch of stuff going on here, but mile-high view:
* Set up a bunch of initial values (necessary for Python not throwing a hissy fit over stumbling across variables in if-statements later on, without them having been defined yet)
* Iterate over each line
* Check if the current line is a separator line (in which case we must already have populated a passport object and could add it to the list of passports (under the assumption that the input doesn't start with a separator, but with passport data, so we won't trigger this check on the first iteration). We'll also update prevLine so that on next iteration, when line is again something useful, we can see that the previous line ended a passport, and we should set up a new passport object, and since this line was a separator, we can avoid wasting any more cycles by jumping to the next iteration immediately)
* Upon next iteration we won't get caught by the above check, prevLine was a separator, so create a new passport object
* And since we have not jumped to next iteration, this line contains useful stuff, so parse it, entering any found data into the current password object
* We will also, again, need to update prevLine to current line, so that on next iteration there won't be any funky stuff (actually this might not be necessary, but I'm crossing the t's and dotting the i's).

And then we just sum up all the valid passports and return.

All good, right? WRONG!

As I said, there is a bug in here. On the last iteration, we have created a passport object, and the last line of both test data and the actual input, both contain data, so there is no trailing separator, and as such, the last passport object is never added to the list of passports.

How, then, could the test pass? Simply because the last passport entry of the testdata was an invalid passport, which would never have been counted towards the expected number of valid passports anyway...

There is probably a lesson in here about randomizing not only the test-data, but the order of the test-data as well. For real live systems at least, perhaps very much overkill for AoC.

### Attempt #2 ###

    passports = list()
    prevLine = separator = ''
    p = Passport()

    for line in data:
        if line == separator:
            passports.append(p)
            prevLine = line
            continue

        if prevLine == separator:
            p = Passport()

        pairs = line.split(' ')
        for pair in pairs:
            key, value = pair.split(':')
            p.update(key, value)

        prevLine = line

    # dumbass! once we exit the loop, we have a dangling passport object not added to the list!
    passports.append(p)

    return sum([1 for p in passports if p.is_valid()])

Shown above: improved, bug-free code.

## 4b ##

> I shall be telling this with a sigh
> Somewhere ages and ages hence:
> Two roads diverged in a wood, and I -
> I took the one less traveled by,
> And that has made all the difference.

Robert Frost -- The Road Not Taken

Today I was not able to foresee how the second problem would build upon the first, how it would be extended. Perhaps extended validation was the obvious next step, but I didn't see it.

So by sheer dumb luck I took the route I usually wouldn't, objectifying the data, and that made all the difference for the second part.

The validation method in the Passport class balloned, from 4a:

        def is_valid(self):
            for field in self._required_fields:
                if self._attributes[field] is None:
                    return False
            return True

To 4b:

    import re

    ...

    PATTERN_HEX_COLOR = re.compile(r'^#([0-9a-f]{6})$')
    PATTERN_NINE_DIGITS = re.compile(r'^([0-9]){9}$')

    ...

        def is_valid(self):
            for field in self._required_fields:
                if self._attributes[field] is None:
                    return False

            if not 1920 <= int(self._attributes['byr']) <= 2002: return False

            if not 2010 <= int(self._attributes['iyr']) <= 2020: return False

            if not 2020 <= int(self._attributes['eyr']) <= 2030: return False

            if 'cm' in self._attributes['hgt']:
                at_least = 150
                at_most = 193
            else:
                at_least = 59
                at_most = 76
            if not at_least <= int(self._attributes['hgt'][0:-2]) <= at_most: return False

            if not PATTERN_HEX_COLOR.match(self._attributes['hcl']): return False

            valid_eye_colors = [ 'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth' ]
            if not self._attributes['ecl'] in valid_eye_colors: return False

            if not PATTERN_NINE_DIGITS.match(self._attributes['pid']): return False

            return True

But that's also all that changed.

Yes, I cheated and used regular expressions for validating the haircolor and passport ID, but what would the alternative be? Checking the length of the string and iterating over every char of it and checking if it was in the list of allowed characters, like a caveman? Jeez.

Also, it should be apparent to everyone that I am a fan of exiting early. I could of course have had a `result` variable, and defaulted it to True, and if any if-statement triggered, set it to False, and returned that at the end of the method, not sure why I do it like this. To spare a couple of CPU cycles to not evaluate the remaining if-statements? Possibly. Was that intentional? Not sure... When I wrote the thing there was no conscious thought about it, I just probably want to deliver a response as early as possible.

## Late addition ##

Finally got the AWK-solution working for 4a.
Not as trivial as first expected, my AWK skills are seemingly fading... but now knowing what 4b entails... I ain't gonna go near that shit with AWK... ;D

But it was fun (and frustrating) getting 4a to work in AWK.
