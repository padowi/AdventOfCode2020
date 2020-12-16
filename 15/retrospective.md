# Retrospective #

This days task gave me more problems than I'd care to admit (well, at least 15b did), as evidenced by the git log:

    commit e25a3e4b93df968a24bf7cb644cc4a75df7b5d1a
    add solution for 15a

The above also added a failing attempt at 15b, which was followed by another failure:

    commit 7e646b77a86cdb8b7f14cf39e95a87ab2878547d
    another unsuccessful run at 15b

Which was eventually followed by:

    commit f841de9df1abb618c1d0d7a8adadfa1bf02ac52a (origin/main, origin/HEAD)
    add potential solution for 15b

    can't verify on my RPi as it just hangs/becomes unresponsive on the
    larger testcases (30M target)

    commiting so that I can pull on another system, for over-night runs


From previous days you will have noticed that my aptitude in maths is basically non-existant, so when an algorithmic response is necessary, I'm pretty much stuck. Unless I can somehow easily bruteforce my way into finding out how to construct the algorithm needed. But that is highly unlikely.

There is of course another potential way forward: If the bruteforce way is just a tad bit too slow, then optimization might be the way to go. This was how I dealt with 15b.

But first:


## 15a ##

The task is fairly straight forward. You get a bunch of input numbers as seed values, and two rules:

* If the latest (previous) number spoken (beginning with the last of the seed numbers) has not been spoken before, the next number to be spoken is 0
* Otherwise, the latest number had been spoken before (and again, just in the previous turn), and then we should calculate the delta between the last two occurrences that number was spoken, and this delta is our next number to be spoken.

The naive approach is to set up a list (hey, we're only expecting it to have 2020 elements in it, so a list should work well enough) and append any new number to it.

I ran into some problems here, as Python strings have an `.rfind(char)` function (find index in string of the right-most occurrence of `char`), but lists doesn't appear to have a similar functionality...

And I didn't savor the prospect of constantly doing either `reversed(numbers)` and ugly-calculating the positions, nor converting the list to string (or for that matter, building a string one number at a time).

On the other hand, how hard can it be to write an `rfind(item, sequence)` function myself?

    def find_last_occurrence_or_add(x, seq):
        # damnit... the way I am structuring runner below,
        # I'll never get to use this fancy function... :'(
        # I wrote it as a tracer before I had read the full requiremens...
        # so now instead of this, I'll just build some other function
        # that will make more sense for the task, but I like the ugliness
        # of this function so very much that even though it is dead code
        # I'll leave it in here.
        for i in range(1, len(seq) + 1):
            try:
                idx = seq.index(x, i * -1)
                if True: # what a nasty piece of ugly-hack you are, I love it!
                    break
            except ValueError:
                continue
        else: # woho, finally got to use for/else!!!
            seq.append(x)
            idx = len(seq)

        return (seq, idx)

So I wrote this ugly mcuglyface function. It is so ugly that it becomes beautiful. Unfortunately, the more I thought about the overall structure of the program, not just this one little implementational detail, the more I cam to realize that this little ugly fucker would never fit into the process... I left it in the source code because it is too unique to die, yet too useless to be used.

But now I am well into the sidetracks again...

So I ended up writing another wildly inefficient piece of shit:

    def diff_last_two_occurrences_of(x, seq):
        indices = list()
        for (idx, num) in enumerate(seq):
            if num == x:
                indices.append(idx)

        return indices[-1] - indices[-2]

Enumerate all items in seq (this gives us a tuple in the format `(positionInSequence, elementValue)` (which I promptly named `idx` and `num`.
If the number returned in each iteration is the number we seek, append the location of that number to a list.
Then return the last number in that list, minus the next to last number in that list.

Sidenote: A buddy of mine from university once ran a blog, with the tagline _"Clever, yet cute"_. The above code is neither.

But it got the job done, so whatevs.


## 15b ##

Ooook... instead of the 2020th number, we're now looking for the 30_000_000th number (yes, that's a valid (and very humanly readable) way of writing 30 fucking million in Python)

So... obviously my slow piece of shit code from above won't work. I did some lame attempts at optimizing the code from 15a, but it just ran into the wall faster: Python + a list approaching 30M elements + a poor Raspberry PI 3b == complete and utter failure.

So, we needed a new angle of attack. Big brain time! I actually managed to optimize the solution, instead of the existing code.

It is of course daft to record EVERY single occurrence of numbers spoken, when we'll ever only care about the last two occurrences, and at that, only their locations.

And it isn't actually _"locations"_, it is at what iteration they were spoken, but it became locations in my head, when I chose to chuck them all into a list in 15a.

So, instead of a list of 30M integers (if this was C, that would be int[30000000], and each int is what? 32 bits? 4 Bytes * 30M might not be all that much, but it is a heck of a lot when it is unnecessary.)
Also, apparently Python is not optimized for retrieving stuff from the back of a large list.

But it doesn't matter, I discovered in a previous day that Python has a ring-buffer like structure: `deque()` with the `maxlen` parameter.
Chuck that into a dictionary, where the number spoken will be the key, and the deque will be updated with the current iteration and we have something fairly more efficient.

We'll of course need a new variable for tracking what the most recent spoken number was, but that is a single number. And we need a loop, which is working its way towards 30_000_000.

[My colleague](http://www.github.com/henkla/adventofcode2020/) did that big brain thinking already in 15a, so while I had to gut my entire 15a solution and rewrite it from the ground up, he was just like _"oh, ok, I guess I'll change `2020` to `30000000` and run it once more..."_

And this solution was still too much for my poor RPI to handle, so I had to clone the repo on my desktop and run it there. But hey, it got the job done.


Overall, this task was fun, it gave me a fair bit of trouble, but it wasn't a problem that were many orders of magnitude away from solving, so while I did have to change how I approached the problem, I still managed to come up with a better _"bruteforce"_ solution. So all in all, fun :)
