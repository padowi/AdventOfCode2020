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

Perhaps I should also attempt to explain that code...

So, AWK has a bunch of magic variables that determines how it parses stuff. RS (Record Separator) and FS (Field Separator) being the relevant ones here.

We know that our input will have passport entries separated by a blank line, so our AWK record (a passport) is separated by two newlines (the newline ending the last line of the previous record, and the newline immediately after it, marking up the empty "separator" line.

Now that we have established the boundaries of the records that AWK will work with (Unlike grep, AWK does not need to operate on a line by line basis, but the default RS is "\n" which makes it function like grep, working with one "row"/"line" at a time.

But in our BEGIN-header, (another special magic directive, which is guaranteed to be executed by AWK before any input file is read/parsed) we override that, so now what AoC considers a record (passport), AWK will also consider a record.

$0 is a special variable, and it will contain the entirety of the record currently being processed.

Next we have the Field Separator, it defaults to "any whitespace" (i.e. something akin to `FS="[ \t]+"` (yes, I know there are more sorts of whitespace than tabs and spaces, but I'm tired...)

We reset that to be either a space or a newline. So now, within our record, whenever AWK sees a space or a newline, it will know that a field just ended, and a new one is about to begin.

Each field is assigned an index, starting with 1 and incrementing upwards. (It couldn't start with 0, since $0 is reserved for the whole record itself).

In the BEGIN header I also set up an array (more like a dictionary, but AWK doesn't seem to have the concept of lists/sequences, so I had to make do), containing all the required passport fields.

This array (`required`) will have the layout
* 1: byr
* 2: iyr
* 3: eyr
* ...
* 7: pid

We also set up a counter, `valid`, defaulting to 0. Whenever we happen upon a valid passport, we will increment this.

We also have the special magic END rule, guaranteed to not execute until the entire input file has been processed, and in that we simply print the number of valid passports to the screen.

Left to break down is the single rule that processes all the records.

AWK programs usually follow a `RULE { ACTION }` syntax, where RULE is usally some type of condition, which, upon evaluating to true, triggers any and all action statements between the curly-braces.

AWK has defaults for both RULE and ACTION, so in the event that one or the other is missing, it will still do something.

In the absence of a RULE (like in my code, which starts with a curly-brace on line 8) AWK will simply use the default, which is `True`, and since True usually evaluates to... well, True, the ACTION part will trigger for every record found in the input file.

(For completeness, the default ACTION if none has been provided, is `print $0` (i.e. print the entire record))

I have a fleshed out action however.

First I iterate through every field in this record, from i=1 (remember, fields inside the record starts at 1, since $0 is taken to output the entire record) to NF (another magic variable, **Number (of) Fields (in the Record)**

For each index, (`i`) we ask AWK to access the contents of that field (`$i`) and we use split on that field, with a colon as the separator, to create a temporary array *pair*.

pair[1] contains the key (e.g. byr or pid), and pair[2] contains the value given to that field in the input.

I then just pull another variable (another array) out of thin air (*passports*) and start mashing data into it.

Since we are doing all of this inside a loop, hunting for all the passport field-names, we couldn't pick and choose, that would have been nice, then we could have used the passport pid value as the key in the passports array, but then again, perhaps that isn't unique in the input, so instead we use yet another magic variable NR (**Number (of the) Record (currently being processed)**).

That is as unique an ID as we are likely gonna get. And AWK just gave it to us to use, just like that, without us even asking. Good guy AWK.

Why do we want to separate all the passport records into their own entries in the passports array? Good question, we could have made a 1-dimensional temporary passport array instead, since we only use that entry in the current iteration, and never again...

Anyway... then we create a temporary score variable, this will be overwritten for every new iteration, we're OK with that.

Because up next is iterating over all the required fields (well, if you remember above, the required array looked like 1: byr, 2: iyr, etc) so we are iterating over all the keys (1..7) and then accessing the value (byr, et al) from the required array, and checking if that field name is present in `passports[NR]` (i.e. the current entry), and if it is, increment the score.

Once we have iterated over all the required fields, we check if the score variable contains 7 (I got lazy, and couldn't be arsed to figure out how to get the length of the required array, it is probably size() or count() or something, so instead, yeay, magic numbers in the code \:D/

If the score is 7, it would indicate that the above loop managed to find all the required fields in the current record. Which means that this passport is valid, so we increment the valid counter.

235 lines of English gibberish to explain 23 lines of AWK later: We are done for today!
