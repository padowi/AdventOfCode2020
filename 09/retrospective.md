# Retrospective #

So today I did something new. An implementation plan (or perhaps "proposal").

A design-document thingy for outlining what I thought the solution might
possibly look like.

At this point it might be interesting to compare the IP with the actual code.


## 9a ##

I got the parsing function to convert the numbers in the input to integers
straigth away, this is such a tiny implementational detail that it should
probably not have been in the IP at all, but I put it in there, and remembered
it when it came time to implement the actual solution. Nice.

The code for dealing with whether or not the current number is a valid/invalid
number is not as beautiful as I'd like it to be. It is clunky even.

My colleague had [a much better implementation](https://github.com/henkla/AdventOfCode2020/blob/d4dfa086cd9e3193d0ea645a2621e41022ed60ef/Day09/Program.cs#L121-L130) than me. (Which he later on refactored, but this one is more beautiful than mine.

Sidenote, one of the lecturers in one of my programming classes back in
university had the following to say about code:

> First make it work, then make it beautiful. If needed: optimize.

So technically I am still in phase 1. It does work, [but is ugly as sin](https://github.com/padowi/AdventOfCode2020/blob/main/09/a.py#L26-L39).

Here I actually think that my IP hampered my thought process, as I had already
figure that I'd need to account for that special case, and didn't do any
additional thinking about neater ways to solve it. Bad Patrik! Bad!

I opted not to go with a full list of all numbers, in which I'd need to keep
track of a pointer to the beginning of the *"X previous items"* window, but
instead, since `collections.deque` exists, does what I want, AND comes with a
the fancy `maxlength` parameter, it was almost like this structure was made for
this type of problem.

collections.deque, for those not familiar with it (this includes me so I
shouldn't write this) is a rather good choice if you are building some type of
queue.

It has a method `append()` which adds an item to the end of the sequence, and it
has a method `pop()` which removes an item from the beginning of the sequence.

And from previous years of Advent of Code I learnt that it does these operations
lighting fast. Like O(1) fast. To me this suggests that the underlying storage
format is a linked list, which ought also mean that lookups (like `x in deque`)
ought be a bit slower, but since we specify the maxlength (25) that should be
too small a number of elements to matter like at all anyway.

I did write a helper function (`is_valid(prevNums, curNum) -> bool`) and it
worked like a charm. (Except for the above mention that it is an ugly
implementation.

The sample data had two formats today.

One actual (but reduced) example, wherein the *"preamble"* was only 5 items
long, as well as a bunch of smaller examples where the full length preamble was
used, but fixed to contain the numbers 1..25. The problem stated they were given
in a random order, but since all of them would fit in the preamble, and the
examples were all marked as the 26th digit, none of the values from the preamble
would be pushed out (or at least not in a capacity to affect the test itself).

So I did write another helper-function, for running the full-scale (but reduced)
test.

Overall, I followed the IP fairly closely, and with the exception of my above
ugly code in `is_valid()`, the IP did not impede me.

Will I do one for every problem henceforth? Probably not. When I code stuff I
usually do a small implementation plan-ish thing within the source-code file
itself, using comments. Once I have something I feel should work, I just insert
a new line under the comment, and add in the code that would do what the comment
outlined.

It is far more likely I'll do that.

## 9b ##

Once I had finished 9a, I actually went through the trouble, even though I was
on a roll and should just have kept coding, to fill out my thoughts about 9b as
well.

The way Advent of Code is set up, that you only receive the second task after
the first is done, and my own setup, reading the problem (a) before work, then
mulling it over in my head until lunch when I attempt to solve it, makes it
harder to maintain the interest in continuing to work with the IP for the
b-problem, since I'd rather take a shot at solving the b-problem, rather than
writing about potential ways of solving it. Especially since I'm already in the
zone from solving a, and would like to get b solved in the same sitting.

And the second paragraph of the 9b subchapter bears traces of this, since it
basically says "fuckit, I'm going bruteforce.

I did go out of my way to visualize how I imagined it would perform its task,
and that is how it ended up working as well.

It is wholly possible that I would not have thought about the optimization I
could do (i.e. short-circuit the inner loop if our summed slice ends up bigger
than the target), so it does have that going for it.

On the other hand, this is probably something that the *"IP-light"* (comment
outline in the source) would have caught as well, had I used it instead.

Tomorrow I'll try to remember using the Comment Outline technique instead of an
IP.

As for the problem itself, I do wonder what a "better than bruteforce" solution
would look like.

Too tired and not enough overall math-smarts to even begin considering this. So
that's all for tonight.

:wq
