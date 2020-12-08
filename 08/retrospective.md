# Retrospective #

Got a real intcode vibe out of this problem. Not sure if I'm happy about it, or scared.

The problems were fun, I encapsulated the problem with a class, and abused Exceptions as my only channel of signalling back to the runner that the execution had come to some sort of milestone (whether that was a detected loop, or end of instruction set).

In retrospect (hey, that's this here file, ain't it?) I could have made the `step()` method return True on success and our desired value on failure instead.
That would have been so very much cleaner than my fuck-ugly "ReadyToBootError" which isn't an error at all, but just a signal that we've reached the end of the line and boot process is ready (yeah, so the name of the error is doubly wrong...)


## 8a ##

This one was fairly straight-forward, go trough the instructions one by one, keep a record of instruction positions the cursor has already visited, and if we hit one of those again, we have a loop.

Here the *LoopDetectionError* exception may actually have been the cleanest way to go about it, I don't know how else I would have gotten the accumulator value out of the instruction method back to step, and told step that we found a loop, ok probably the same way as step would signal it to the outside caller, True or desired value...

I am speeding through this problem, because it really was straight forward, and not all that interesting.


## 8b ##

Here, however, was an interesting problem.
So our input data is corrupted. More specifically, a single line has gotten either a 'jmp' or a 'nop' flipped. We are told that we need to perform a single change to the program to get it working.

Since I am a retard my first instinct was "Ah, a nail! HAMMER DOWN!" I mean, how many 'jmp'/'nop' can there be in the input? 224 and 55 respectively. Well shit.
Furthermore, from the sample test data we can gather that not all of those instructions will even be touched by the cursor...
So not only would we create an insane amount of copies, we'd also do most of that busywork for no benefit.

Think Patrik, THINK!

OK. Instead of just blindly making copies, altering a single instruction in each, for every instruction in the data, and then running a computer for each modified datii, what if we run the original program once, but instead of extracting what the accumulator had gotten to on loop detection, we instead sent back the list of instruction positions which the program cursor had actually touched?

And from that much smaller list, filter it even further, removing all the 'acc' instructions, leaving us with just a few  'jmp'/'nop' instructions.

How does this help? We've reduced the search space immensely, that's how. And since are only allowed to make one single change to the program, the solution lies in changing one of these instruction positions.

A smart person might have done this iteratively, only taking the original data * 2 memory (original + currently modified copy) into possession. Not me, nosiree, I created clones of the data for each of the positions I'd change, then changed that one individual position in each clone, and THEN I started iterating over them, one at a time.

So many things I could have done better here, where I don't even know why I didn't. But hey, it worked out anyway, dinnit?
