# Retrospective #

I solved both of today's problems fairly quickly, but stumbled a bit on 1b before solving it.

For 1a I simply saw a nail, and applied a hammer, brute-force style:

    while numbers:
        num1 = numbers.pop()
        for num2 in numbers:
            if num1 + num2 == 2020:
                return num1 * num2

For 1b I thought that I could get away with using the same basic concept, but pop off two items at a time.

This was of course mighty stupid, since I had a while data loop, which means that for every iteration I would remove too many pieces of data that I had not yet vetted against all the other combinations.

I was stumped for a while until I just realized it. At the same time it hit me that if I could just generate a list of all the various (unique) combinations (regardless of which position each number would have in the tuples returned) (i.e. I wanted combinations, not permutations), and apply sum to each of these items, compare that with the target number (2020) and in case of match, apply multiplication on that item, and return the result, then I'd be done.

    for pair in itertools.combinations(numbers, 3):
        if sum(pair) == target:
            return math.prod(pair)

Very clean, very slim, yet not overly terse. It is beautiful code, because it is easy to follow what is happening.

It is also beautiful because it works.

So I set out and refactored 1a to do the same thing:

    for pair in itertools.combinations(numbers, 2):
        if sum(pair) == target:
            return math.prod(pair)

Note how the only difference here is in itertools.combinations, how many items should go into each pair-tuple.

So all is well and good, right?

Well, I did solve it so yeah, kindof, but this is introspection hour, not pat-yourself-on-the-shoulder hour, sooo:

A colleague used a different algorithm than me in 1a:

    for num1 in numbers:
        if (target - num1) in numbers:
            return num1 * (target - num1)

Well, that is basically the code, but he used C#, not Python.

The above code does however accurately represent the concept of his solution:

> For every number, subtract that number from target, and check for existence of this difference within the collection of numbers.
>
> If it exists, then we take these two numbers, multiplying them, and returning the product.

I wish I could think of such solutions, but I don't, and most of the time, the problem spaces are small enough that even with the paltry hardware of my Raspberry Pi 3b, the problem yields before my application of enough force.

For 1b he confessed to not having the time nor energy to think of a proper solution, and simply nested a couple of for(each)-loops.

Since I was curious about how my solution would fare against his, I attempted to apply his concept on 1b:

Original code:

    for pair in itertools.combinations(numbers, 3):
        if sum(pair) == target:
            return math.prod(pair)

Improved code:

    while numbers:
        num1 = numbers.pop()
        for num2 in numbers:
            if (target - (num1 + num2)) in numbers:
                return math.prod(num1, num2, (2020 - (num1 + num2)))

Now, by just looking at them, I still consider the original code to be clearer, and more to the point.

But timing the code (`$ time b.py`) when running the original code, yields 2.5s of runtime. And for the improved code, the runtime is 0.3s.

This is not exactly mind-blowing, my original code generates a shitload of extra data (the combinations), all of which is plowed through.

My original idea was always to attempt to reduce the number of necessary checks, which is why my original 1a popped off a value on each iteration, to make the next iteration run just a tad bit faster.

With itertools.combinations I threw that out the door and went full brute-force.

But by gradually popping a value, and using that, along with every other value in the set and using those two numbers (summed) and subtracted from the target, to generate the third number, and checking for the existence of that number in the set, I am essentially marrying my reduction-solution with his derived lookup solution, and that will be many times faster than generating a much larger data set, and looking through it.

NOTE: For 1a, the difference in runtime between my itertools-solution and his derive lookup-solution is much smaller (still to his advantage though).

So between the fact that I still can't write performant solutions, and I stumbled like a buffoon over popping too much at the beginning of 1b, I am still not the world's best programmer. Shocker, really...

The only remaining question is: how can I make this lesson stick? This was a really nice way of approaching the problem.
