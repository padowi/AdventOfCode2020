# Retrospective #

Today's task (well, 13a at least) was fun. Good simple fun.

## 13a ##
I could not get to a real computer until some time after lunch, but had "coded" up a potential solution in my smartphone notes-app about 15 minutes after reading the problem.

I ended up missing to account for `break` only working on the inner loop, but my first attempt got me 95% or so of the way.

It went something like this:

    initialTS = ts = int(data.pop(0))
    buses = [ int(bus) for bus in data.pop(0) if bus != 'x' ]

    while True:
        for bus in buses:
            if (ts % bus) == 0:
                break
        ts += 1

    return bus * (ts - initialTS)


There are two problems in here:

1. the list comprehension for extracting valid buses (line 2 in above code) will iterate over a string, i.e. multiple occurrences of <digitOrX><comma>
   I needed to add a `.split(',')` on the back of `data.pop(0)`
2. line 6 above contains `break`. My idea here was that it would break the `while True` loop as well, thus going straight to the return.
   Of course it only broke the inner loop, going on with line 7, and thus jumping back for another `while True` iteration

What I ended up with is:

    initialTS = ts = int(data.pop(0))
    buses = [
        int(bus)
        for bus
        in data.pop(0).split(',')
        if bus != 'x'
    ]

    endLoop = False
    while not endLoop:
        for bus in buses:
            if (ts % bus) == 0:
                endLoop = True
                break
        if not endLoop:
            ts += 1

    return bus * (ts - initialTS)

And this is of course a load of horseshit. Setting a variable to determine whether or not to continue the outer loop might seem smart... until you realize that you need to check that variable again inside the outer loop to check whether or not we should be iterating the timestamp.

Yes, we could have done something ugly like

    initialTS = ts = int(data.pop(0))
    ts -= 1

    ...

    while not endLoop:
        ts += 1
        ...

to get around that last if statement, but the obviously more correct solution would have been something along the lines of:

    while True:
        for bus in buses:
            if (ts % bus) == 0:
                return bus * (ts - initialTS)
        ts += 1

So I finally get to a computer, work out all these kinks (except for making the code beautiful like the previous codeblock above), get the right answer aaaaaaand...

## 13b ##

Is another one of those shitty math-solution only type of problems which I am unable to crack.

I have **NEVER** been good at math. Logic, yes, math, fuck no. I just don't *"see"* math the way people who understands math sees it. I can't blame it on crappy teachers, because my peers seemed to get it. I'm just wired... differently. And these problems hold absolutely no value to me.
(Probably because I can't even attack them, so they are the very definition of un-fun, which is more or less the only reason I participate in Advent of Code at all, to have fun.)

Will I try to solve it? Yeah sure, some time when I have the time (yeah, the same kind of *"some time"* as *"I'll for sure go back and fix that tech debt that crept up on us during this sprint, uh-huh..."*

No disrepect to the organizer(s) of AoC though. It is a valid problem, just that this dipshit here can't solve it (well of course I can, just go to /r/adventofcode, look for a 2020-13 python thread and steal their solution, BAM! done, but how satisfying would that be?)
