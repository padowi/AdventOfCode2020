# Retrospective #

Upon first reading the problem, sometime this morning, I started thinking about possible solutions. I remembered a previous year had a somewhat similar problem, where you were supposed to traverse a corridor of lasers or something, and you had to model how they moved back and forth, and I found myself thinking that I'd need a list (one entry per row) of either `collections.deque` or `itertools.cycle`.

That would probably have worked, given enough code (for each row I iterated over, I'd need to call `next` (or `pop`/`push`) as many times as the index of that row in the list). Seems like a hassle.

Fortunately I stopped myself before even reaching for those tools, and instead made use of a really neat fact about Python. Strings are iterable, and you can consider it to be a list of characters.

The problem also told us that the input was a graph that stretched on infinitely to the right, repeating itself over and over.

Instead of thinking about the problem input, or the example, let's just consider a string "ABC", which, in the scope of this problem, would repeat itself indefinitely ("ABCABCABCABCABC...").

And since a Python string can be iterated over like any other list, let's represent the string that way instead:

    mystring = ['A', 'B', 'C']

Python, like most things, is zero-indexed, so `mystring[0]` would give us **A**, etc. Simple stuff.

    len(mystring) # i.e. getting the length of the list/string

yields **3**, because three characters in the list.

Suppose we wanted to iterate over all the characters, but using say... `for idx in range(1000):`. Doing `mystring[idx]` would work the three first iterations, and then we'd get some *index out of bounds error* because we read beyond the length of the list.

Here's were the modulo operator shines.

    for idx in range(1000):
        mystring[idx % len(mystring)]

This would become

1. `0 % 3` (which is 0), so we get an **A**
2. `1 % 3` (which is 1), so we get a **B**
3. `2 % 3` (which is 2), so we get a **C**
4. `3 % 3` (which is 0 again), so we get an **A**, again
5. `4 % 3` (which is 1 again), so we get a **B**, again
6. `5 % 3` (which is 2 again), so we get a **C**, again
7. guess what number `6 % 3` will yield... I dare you ;)

We have successfully constructed something which will loop over the contents of a list (or, at least in the case of Python, optionally a string).

Since the input is an ASCII art map filled with lines of text (i.e. a list of strings), this is useful.

OK, so the problem also stated that for each step down, we go three steps right.

Since the problem was speaking about angles, and gave both down 1, right 3 as inputs, I constructed a function that would expect both. Just on the face of it, it wasn't strictly necessary to grab the "down 1" parameter, as we already knew for the first problem that we'd iterate over all the lines, but I assumed that the 3b task would have us ... I don't know, figure out which angle from *down 1, right 1* to *down 10, right 250* would be the one without any trees... so I made space for the down parameter as well.

Now, while we are merrily iterating over all the rows in the input, with our ability to cycle through the characters of the row, we need a way to know how much to cycle. We start at x:0,y:0, so second iteration would find us x:3,y:1, and after that x:6,y:2, then x:9,y:3.

There is a pattern emerging here. On row 0, we are 0 steps in. On row 1 we are 3 steps in, and on row 2, 6 steps, row 3, 9 steps.
We were supposed to move three steps right for each row down, and if we have the index of the row, we could simply multiply that number by the number of steps, to know where in the *"infinitely"* long string we'd be.

Since Python doesn't have a real `for (int i=0; i<...; i++)` loop construct, where *i* would be this row index, they have seen it fit to provide a helper function: `enumerate(iterable)` returns an iterable consisting of tuples, *(row index, row content)*

    stepsRight = 3
    for idx, row in enumerate(playingField):
        char = row[(idx * stepsRight) % len(row)]

And since the exercise was to count how many trees we'd hit on this path, we simply need to have a counter, starting at 0, and incrementing it once for every time the identified char was a tree symbol (#).

Since other problems in previous years have been possible to model and solve in this fashion, this didn't present me with much of a problem.
The hardest part was remembering how modulo works i.e. in which order to put the components (had I not been a retarded chimpanzee when it comes to math, this would probably have been intuitive to me).

Looong story is long, all for me to humble-brag that I solved it real easy.

On to 3b.

This problem brought me back down to Earth.

The sample test data says that those slopes would yield 2, 7, 3, 4, and 2.
Only the last of those slopes is problematic, since on that one, we're skipping rows, so for the longest of time I instead got the output 2, 7, 3, 4, and **1**

I finally figured out that my beautiful algorithm from 3a, wherein we multiply the row index by the stepsRight, fucked everything up, since we were now skipping every other row, but had already gotten a row index assigned for those skipped rows as well, our right shift was going haywire and we ended up further right than we should have.

So in the end, since the *"beautiful algorithm"* worked for all entries where down was 1 (i.e. iterate over every row), I broke out calculation of the x position into a variable, and made the code ugly with multiple if statements to check whether or not we were iterating over every row, or just some, and only when we hit an actual non-filtered row, we'd check what row[x] contained.

I initially tried to set x for down > 1 in the same if-else conditional before the check, but this too screwed me over, and in the end it was far simpler to just reason that *"OK, we didn't exit the loop early, we've collected whatever data we wanted from this iteration, and we got this far, update x in preparation of the next iteration"*

I am not proud of this code. 3b works, but it is shit code.

Like "I went to the zoo the other day, but it was really bad, had only one animal, a dog. It was a shit zoo (Shih Tzu)". ;D;D;D
