# Retrospective #

Another problem where the input is separated by an empty line, might this become a trend for AoC 2020 such that we should put some time into writing utility functionality for parsing this type of data?

Could be a fun exercise anyway, we already have two problems we could test a solution on.
It could probably be as simple as a function with three arguments: the input data to parse, what (if any) are the field separators within this data, and ... possibly... this might be biting off more than I can actually chew... the datatype we want the parsed input stored in (but this can become really complex, perhaps a much easier, and more attainable goal, is to always just return something like a list of dictionaries or something.

Anyway, on to the actual problem!

## 6a ##

So the problem text not withstanding, each "record" (separated by a blank line in the input) represents a group of people travelling together, with each line representing a specific individual.

Each individual (non-blank line of input) has filled out a series of characters representing where in the customs declaration they answered "yes".

Our task is to figure out what questions any individual (divided by group) answered yes to. But if two members of the same group answers yes to the same question, that question has still only been answered once by that group.

Once we have a handle on what groups have collectively answered what questions, we can sum up the amount of questions answered by all the groups, and that would give us our problem answer.

Since we don't care about multiple replies to the same question within the same group, but we do give a shit about it between groups, I came up with the following idea:

We need some initial setup, an index variable, and somewhere to store our results, that could be separated by that index variable.

For this I created `groupID = 0` and `declarations = defaultdict(set)`

`collections.defaultdict` is a Python *"batteries included"* type thing. It will create what is in essence a Python dictionary, but with the added property that when you try to access a key within this dictionary, if that key doesn't exist, it will be brought into existence, with a default value of the type specified when the default dict was first created.

So in this case, I have a default dict where each new key being accessed, will instantiate a new (empty) set.

And a set is a data structure not unlike a list, but with a few differences:

* Python does not guarantee that the ordering of a set is static (so sorting a set is nonsensical from python's perspective), and
* Whilst the same value can occur multiple times in a list, if you attempt to add a value to a set, and that value already exists within the set, the set will remain the same before and after the attempted adding.

For our purposes, this is perfect.

This means that I can iterate over all the input lines, and while I am not hitting an empty line, I can merrily add whatever characters are represented on that line (one at a time), into the set identified by the groupID variable (using it as the key in the default dict).

If I happen to add the same character twice, set don't mind, set don't give a shit (to paraphrase [the nasty-ass honey badger](https://www.youtube.com/watch?v=4r7wHMg5Yjg))

And this is just what we want. The same group, the same question, only accounted for once.

Once I hit a blank line, increment the groupID, since next iteration will be a new "record" containing data for a new group. I also make sure to jump to the start of the loop again, to begin the next iteration, since this empty line per definition won't add anything of value to the result.

Once I have looped through every line in the input I grab the length of all the sets in the dictionary, and sum them up, returning that sum to whoever requested it.

So, instead if `return sum([len(val) for val in declarations.values()])` I could have written:

    result = 0
    for groupAnswers in declarations.values():
        result += len(groupAnswers)
    return result

There's a time and place for everything, list comprehensions *can* muddy the waters so perhaps the more verbose alternative is better. But for Advent of Code...? Nah. I'mma use it.

And to beat this poor dead horse even further, there is nothing that forces you to define a list comprehension on a single line:

    return sum(
        [
            len(groupAnswers)
            for groupAnswers
            in declarations.values()
        ]
    )

Is completely valid code. Onwards!


## 6b ##

6b was difficult because I didn't read the assignment. (This will get you almost 100% of the time, unless you aren't terribly lucky.)

So, on the first reading of the problem, I got it in my head that only the questions which had been answered yes (i.e. being present in the input data) by EVERYONE in the group should be counted (this part of the problem I got right) and that they should be counted as many times as the group members had answered them.

So in a group of 3, where all three answers yes to "a", I figured that we shall count this answer (correct) all three times (incorrect).

So I did:

    if value == memberCount:
        result += value

When instead it should have been a much simpler:

    if value == memberCount:
        result += 1

Sure fine, but all this depends on actually getting the data so we can count it. How did I get here?

First of all, this time around, we ARE interested in how many times an answer is represented within each group, so we can't just stuff it into a set anymore. (Well, we could, but it wouldn't help us in the slightest.)

Another thing we are interested in for this problem, is keeping track of how many people there is in each specific group.

We are still using the same input, so the same basic principle for parsing the data exist:

Loop through each line, upon a blank line we have reached the end of one group, and should begin a new group.

The thing that varies is what steps we take while processing each line within each individual group.

For each group we need to figure out how many members there are to the group, and for each question answered "yes" by a member of the group presently being processed, how many times this question was answered.

I could have built a custom class, *"GroupDeclaration"* or something... Instead I opted for something simpler: `defaultdict(dict)`.

So this is a dictionary, which when asked about accessing a key it has not yet encountered, will respond with shoving an empty dictionary in the callers face.

Since each line in the input, excepting blank lines, represent a single individual, this means that for every line we encounter, up until the next blank line (or end of lines), this is +1 group member in whatever group we are currently working with (`groupID`, which is incremented upon finding a blank line).

So for each line we increment the memberCount key (first time we try to access it it won't exist, so we use `.get(key, defaultValue)` (key here being memberCount, and defaultValue being 0))

Then for each character (question identifier) we chuck that in as a key in this groups dictionary, and increment the value (again, if this is the first time it is being used, we make sure to get a default 0 out of it first, so we have something to add the +1 to)

This means that if person on line 1 has answered "a", this group (groupID 0) will have a dictionary filled with `memberCount: 1, a: 1`.
If a person on line 2 has answered "ab", the dict will be updated to show: `memberCount: 2, a: 2, b: 1`


The calculation part, where I fucked up (see beginning of subchapter 6b for a refresher), is a fair bit more involved than the simple one-liner in 6a...

Well, it became more involved, because of the way I chose to store the data... Good work dumb-ass...

First of all, for every group we process, we will need to access that group's memberCount.

We will also NOT want that particular key/value pair to show up as an answer which we are checking against. Because what we want to do if check, for each answer, if the integer there matches the member count, in which case all the group members said "yes" to the same question.

So we extract that value, into a temporary variable, and then we promptly remove that key/value pair from the dictionary.

We can then, safely, iterate over all the (remaining) values of the dictionary, and check if there has been as many yes-answers to that question, as there are members in the group.

If this happens to be the case, we should increment the overall count of questions unanimously answered yes by a group.

Funnily enough, I thought that the input parsing loop today felt much leaner than the one in 4a, but looking back at it, there isn't all that much of a difference. Peculiar.

I didn't really gain any new insights into what I could have done instead today. Well, both of today's problems would probably have been very easy to solve with AWK, but I will have to check the solutions of my colleague(s) to see if I can expand my horizons a bit.
