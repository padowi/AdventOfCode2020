# Retrospective #

These two problems were fun, once I understood them. 14a was not really problematic to decipher, I interpreted the problem description and wrote a solution based on that interpretation, and both test and real data passed on that solution, so I guess my interpretation was correct, but I was not certain about it at all.

For 14b, I just couldn't figure out what it was he wanted me to do, and I were left with two choices:

1. Blind trial and error until I got the test to pass, or
2. look at someone else's code and try to figure out what they had done.

I went with option #2, and tried to figure out what (value) I should write into which addresses.

As soon as I figured that out, I re-read the problem description, and still didn't understand, well, I do, but I still consider it far from clear that this is what we should do.

I consider myself to have fairly good reading comprehension skills, as evidenced by the fact that most of the other problems this and past years have caused me little problem.

On the other hand, others managed to correctly interpret the problem...

And I don't think it is the author who is to blame either, since most of the time the problems are easily understandable.

I am unsure what conclusions to draw from this, but all in all, interpreting the problem was more of a problem today, than actually solving the problem.


## 14a ##

Fairly straight-forward, parse input, if mask: set mask, if not mask, parse addr, value, apply mask to value according to rules, save result in memory at addr.
Once input is exhausted, sum up all values in memory. Boom! Done!


## 14b ##

So, after having struggled with the problem description, the goal here is to again parse the input, but this time, the `mask` should be applied to the `addr`, according to some new rules, and these new rules will cause the one `addr` to potentially balloon into many addresses, all of which should have `val` written to them.

I've never really tried to implement such a thing before, first I considered if there was some fancy tree-thingy available in the Python standard library, but before I even checked I figured I don't need one.

There was a problem the other day, 

I've never really tried to implement such a thing before, first I considered if there was some fancy tree-thingy available in the Python standard library, but before I even checked I figured I don't need one.

There was a problem the other day, 

I've never really tried to implement such a thing before, first I considered if there was some fancy tree-thingy available in the Python standard library, but before I even checked I figured I don't need one.

There was a problem the other day, 2020-07 but I can't remember, and a quick cursory look doesn't reveal anything, where I did something similar, in that I pre-populated a list of things to investigate, and while that list wasn't empty, pop off the top of the list, do the investigation, and if new leads were found, add them at the back of the list of things to investigate.

The problem of expanding all wildcards ('X' in this problem) to both 1 and 0, could be solved in the same fashion.

I am actually quite happy with that code:

    def expandAddress(addr):
        targets = [ addr ]
        addresses = list()

        while targets:
            target = targets.pop(0)

            if 'X' in target:
                t1 = t2 = target
                t1 = t1.replace('X', '0', 1)
                targets.append(t1)

                t2 = t2.replace('X', '1', 1)
                targets.append(t2)
            else:
                addresses.append(target)

        return sorted(addresses)

NOTE: There was no requirement stating that the addresses needed to be sorted, but in the interest of not running afoul any stupid mismatches in the test-code for that function, I simply opted to let Python sort the list in both places (expectedOutcome and returned value) so that, as long as I was expecting the right values, and the the function returned the right values, the internal order was irrelevant.

I'm sure that it incurs a run-time penalty, especially on addresses containing many wildcards, but it ran fast enough for me and my RPi here and now anyhow.

And if it had been a problem, I could just have removed that test-case and the `sorted()` call and gone vroom vroom.
