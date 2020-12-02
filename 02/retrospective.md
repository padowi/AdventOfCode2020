# Retrospective #

When I first read today's problem, my immediate thought, before I'd even completed reading the problem, was that I'd use regular expressions.

I am happy that I did no act on that impulse, as creating that lookup-table, between patterns to look for, and strings to attempt matches against that pattern, would have been horrendous.

Instead I just used good old fashioned string splitting, first on colon, to separate the rule/pattern from the password (keeping in mind to strip the initial space off of the password part), and then again on space, to separate the number-range from the sought character in the rule/pattern part.

Finally a split on the hyphen to create `at_least` and `at_most` variables from the range part.

Then it was a small thing to do `if at_least <= password.count(char) <= at_most: valid += 1` and that's all there was to it.

Part two should have been as easy, except, again, I'm a dumbass.

So I do the same splitting, this time renaming `at_least` to `first` and `at_most` to `second`, and managed to keep in mind to offset the positions by subtracting one from whatever value was stored in these two variables, since Python is zero-indexed.

But then I had two brainfarts:

    if line[first] == char and not line[second] == char:
        valid_password_count += 1
    elif line[second] == char and not line[first] == char:
        valid_password_count += 1`

First of all, while this should have worked, it is ugly as sin. But it didn't work, and I had to break out print-debugging to figure out where I'd fucked up.

`line` here, comes from `for line in data:` (`data` here being a list of all lines in the problem input), which means that `line` contains a full line, i.e. positions, char, password, all of it.

Had I not been a donkey, I could have written 

    if password[first] == char and not password[second] == char:
        valid_password_count += 1
    elif password[second] == char and not password[first] == char:
        valid_password_count += 1

and that should have worked.

It'd still have been ugly as sin, but at least it ought to have worked.

Thankfully, I did mess up there, using `line` instead of `password`, and this put me onto another attempt at restating the problem:

Since we were only allowed to have the char in one of the specified places, not both, we could just extract both chars (in `password[position]`) into a list, and count the occurrences of the sought character, in that list.

The list would contain exactly two entries, so the count could come back either as 0, 1 or 2 (no such character in either position, a character in one of those positions, or the character in both positions respectively).

Which made for a much more beautiful code:

    characters = [ password[first], password[second] ]
    if characters.count(char) == 1:
        valid_password_count += 1

That's about it. Overall this year has not been different from previous years, the first couple of days are seductively easy, just to get the cogs turning again, and then *BAM!* random complexity of every problem until the finish. (Well, I can't know that yet, but the seductively easy start is the same at least) ;)
