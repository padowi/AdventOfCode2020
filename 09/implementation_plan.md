# Implementation Plan #

Oh, wow, a new document.

## 9a ##

Yeah, this problem was fun to read, and I immediately got an idea about how to
solve 9a, so I thought I'd document this here.

In the retrospective later on, it could be fun to compare notes, what I thought
would work, versus what actually happened.

So, according to the problem, we get a bunch of numbers (note to self, the
parser should convert them from strings to integers directly) of which the 25
first is part of the setup, upon which the rest of the problem follows.

The objective is to check each consecutive number in the rest of the input,
against the 25 previous numbers, relative to the number currently being checked.

The checking is done by figuring out if there are two distinct numbers (they
cannot be the same) that when added together, forms the number being checked.

My colleague's technique from 2020-01 should work here as well.

    for each number in thePrevious25Numbers:
        if (currentlyCheckedNumber - number) in thePrevious25Numbers:
            # valid
        else:
            # invalid

Actually, no, for every even number we also need to consider the case where
`currentlyCheckedNumber - number == currentlyCheckedNumber / 2` which should
throw it into the invalid, unless there is another combination which yields the
correct number... hmm this is a real gotcha here.

For the *"thePrevious25Numbers"* part, I have two options:

1. Track how many numbers we're supposed to consider (the larger test data
   sample later in the problem only considers the previous 5 numbers) and have a
   pointer to designate from where the numTrackedNumbers begin, or
2. Find some data structure for which you can define a fixed maximum length, like
   `collections.deque`, set up the maxlength, and never think about it again.

I will go with option 2.

I should be able to write a helper function
`is_valid(deque: prevNums, int: curNum) -> bool` and once that returns false
(invalid) we have the number that should be supplied to the form in 9a.

Thus ends theory.


## 9b ##

OK, so we have found that one bad number, and we have our initial input. And now
we need to figure out what consecutive sequence of numbers add up to that bad
number. Once we have that sequence, we should grab the highest and lowest
numbers, and sum those, to produce our answer.

There probably is something smart one could do, but it sounds like a brute force
approach will get the job done.

So two nested loops, outer one for pointing out the index where we should start
at until the full length of the data, and the inner loop for, from the index+1
to the full length of the length of the data, and for each iteration of the
inner loop, pull out that slice of elements from the data, sum them, and see if
they add up to the bad number.

Optimization: if our sum is greater than the bad number we seek, break out of
the inner loop to start a new iteration of the outer loop, since continuing in
the inner loop would only increase the sum further.

So something like

    [i|j|.|.|.|.|.|.]

Then

    [i|.|j|.|.|.|.|.]

Then

    [i|.|.|j|.|.|.|.]

And if the sum of values between i and j is larger than the sought number,
restart the outer loop

    [.|i|j|.|.|.|.|.]

Then

    [.|i|.|j|.|.|.|.]

Etc.

Once we find the correct slice (producing the correct sum), apply min() and
max() to that slice, and add those two values together.

And that should be that.
