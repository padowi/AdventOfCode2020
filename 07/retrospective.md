# Retrospective #

One of the things I found myself thinking today was that it is a truly nice template I have crafted. The test-scaffolding is an absolute dream in terms of adding not only more test-data, but also extending the parameters sent to the functions called by the framework.

Today, for *"print-debugging"* purposes, I added a parameter `testData=False` to the problem-solving function.

Then, in my test-scaffolding, I added a dictionary-key 'testData' with the value True.

Within the function, I could then add `if testData: print(whateverIwant)` and it all just works.

A better way would of course have been to set up logging or something, or real debugging infrastructure, or more granular tests. I should perhaps focus on that.

More granular tests could be fun, but would also mean putting more effort into splitting things into functions (not a bad thing either). Perhaps that is the big insight of today?

But let's get down to it (hit me with your best shot).


## 7a ##

So we have bags, differently colored, and rules about these bags. More specifically that bags of a certain color **must** always contain a specified amount of bags of a different color.
Additionally, a bag can contain multiple bags of different colors.

The sample data for instance states that *"light red bags contain 1 bright white bag, 2 muted yellow bags."*

So if you ever see a light red bag, you automatically also know that while you are in the presence of a light red bag, you are also in the presence of 1 bright white bag, and 2 muted yellow bags (the three of these contained within the light red bag).

Obviously the rules go on, stating quantity and color of the bags which *those* bags in turn contain.

Fortunately, some bags don't contain any other bags, so there is, eventually, an end in sight for this madness.

And also fortunately, the creator of Advent of Code is not a sadist, so bag of color A can contain a bag of color B, which can contain a bag of color C, but bag of color A cannot contain bag of color A, nor can bag of color B contain a bag of colors A or B, etc.

If that would have been the case, we'd end up in a loop and it would be a mess.

The rules are stated as `<thisColorBag> contains (one or more) <X> amount of <otherColorBag>`.

But the problem which we are tasked with solving it to figure out what color of bags will end up containing, either directly, or by containing a bag that contains a bag that contains a bag that ... eventually contains the one specific color we are concerned with.

So, we get our color, shiny golden bag. And now we have to figure out a way of counting all the unique/distinct colors of bags which may end up containing a shiny golden bag.

In the example data we can, using mark 1 eyeballs, identify two lines where colored bags are defined as containing shiny golden bags:

    bright white bags contain 1 shiny gold bag.
    muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.

Again, note that the amount of golden bags contained within these bags is wholly irrelevant, the only thing that matters is that these two distinct colors, bright white, and muted yellow, will contain shiny golden bags.

OK, but we're not done yet, because there may be rules outlining that bright white bags and muted yellow bags are contained within some other bags, which would make these containing bags containers of shiny golden bags by proxy.

Indeed, we can identify rules where other colored bags contain bright white or muted yellow bags:

    light red bags contain 1 bright white bag, 2 muted yellow bags.
    dark orange bags contain 3 bright white bags, 4 muted yellow bags.

Here is the next trap: BOTH these colors (light red, dark orange) contain the SAME sought after colors (bright white, muted yellow).

And again, we are only concerned with the colors, not their amounts.

So now our tally of bags that can contain shiny golden bags is four (light red, dark orange, bright white, and muted yellow)

We again need to check if there are any other colors which contain light red or dark orange, but as it is a small test data sample, we are in luck, there are no rules in which light red or dark orange is the "contained" colors of some other colored bag.

So the number of unique colored bags that will end up containing shiny golden bags is **4**.

*"Oh wow, great, you've just restated the problem description..."*

Yes, fully understanding the problem is key to being able to solving the problem.

Next, parsing the data, and then structuring it in a way that makes it easy for us to retrieve the follow on data from that, is the second key part.

The given input, as I already spoke about before, is `this contains that`, but since we have *"that"* and wish to know which *"this"* contains it, it would be preferential if we had the data laid out as `this is contained by that, and that, and that` (given, of course, that there are three other colors that directly contains *"this"*

Did I lose you? OK, pseudocode time:

Problem definition could be considered a dictionary, where some colored bag X outlines a sequence of other colored bags, and how many of these colored bags, is contained within:

    bagContains['light red'] = list('1 bright white', '2 muted yellow')

What we need is:

    bagContainedWithin['muted yellow'] = list('bright red', 'dark orange', ...)

Note how we also stripped away the amount, since in this direction that a) makes no sense, and b) wasn't important for the problem anyway.

What does this give us? Now we can ask the dictionary stuff like *"gimme all the colors containing 'shiny golden'"*:

    print(bagContainedWithin['shiny golden'])

Which yields:

    list('bright white', 'muted yellow')

This is progress!

Now we only need to record those two colors, because we will want to count them in a second or so, and also, because we will have to go ask the dictionary the same question, but for these colors. (I.e.: `print(bagContainedWithin['bright white'])` and `print(bagContainedWithin['muted yellow'])` which both outputs `list('light red', 'dark orange')`)

Now, just to also be clear: There will be colors in the input data for which there is no reverse lookup, they aren't referenced as contained within some other bag, but only contains others themselves. You will need to check first if the color you are asking about, is even in the dictionary. If it isn't, well great, you've found an endpoint.

In the sample data, neither 'light red' nor 'dark orange' will be a key in the dictionary.

Which means that once we have checked those, we have no more colors to look up.

For any of this to make sense we need two variables that can store multiple values (i.e. some type of list). I did a little premature optimization opting to use a set in both variables.

So what are those variables for?

The first one, let's call it *colors*, will be for recording all the distinct colors that can either directly, or by proxy, contain the shiny golden bag. Since we are only interested in the distinct/unique colors, we'll eventually count the elements in this set, and that will be our answer.

The second one, let's call it *toCheck* will be populated with any colors returned to us when asking the dictionary.

Wait what?! Isn't these two doing the exact damn thing? For now, yes, but tag along, and I'll show you something really cool.

So, once we have done the input parsing, created our dictionary, and set up our two empty set variables, we do this:

Into *toCheck* we add 'shiny golden'. We don't add this to *colors*, since counting the golden bag itself would be an error.

Now we are ready for doing the cool stuff:

While there are elements in *toCheck*:
1. pop one element from *toCheck*,
2. (premature optimization) check if this element (color) exists in *colors*, if it does, go to the beginning of the loop (starting a new iteration)
3. ask the dictionary if that key exists, if it doesn't, go to the beginning of the loop (starting a new iteration), otherwise,
4. for every returned color, add that color to *toCheck* AND to *colors*.

Eventually, you WILL run out of elements inside *toCheck*, since we are popping the off one at a time, and only adding new ones if we haven't already processed this element, and the element actually exists in the dictionary.

And when you run out of elements, the loop ends, and you are at the end of your program. Count up the number of elements in *colors* and return that.

BOOM! Done!


## 7b ##

In this problem, amounts matter, and we are following the same structure as the rules are written in. The overall structure of the program is the same for both problems, except that since we now care about the amount, we need to make sure to parse and store that as well.

But our dictionary will now read like the rules in the input. `<thisColor> contains <X> amount of <thatColor>` and again, there can be multiple bag colors contained within a bag, so again our dictionary should have a color as key and a list as value. The elements in this list, however, should change, from just color, to a tuple `(amount, color)`

No, wait, you don't have to use a tuple, use whatever you want, as long as you store both amount and color together, and that is one element among other elements also storing amount and color.

Again we populate *toCheck* with 'shiny golden' and go to town.
But instead of a *colors* variable, as a set, we instead create an integer *bagCount* with default value 0.

In our dictionary, if we ask it about 'shiny golden', it should now reply with `list( tuple(1, 'dark olive'), tuple(2, 'vibrant plum') )`

Now, for each of these elements, grab the amount, add it to bagCount, and then ALSO, as many times as amount ... well "amounts" to, add that color to *toCheck*.

Waittadamnminute! Adding the same color to a set would only result in it being added once!

True! *toCheck* must now be a list, capable of storing the same value multiple times. Good catch!

Again, eventually we will run out of elements in *toCheck*, this time because our dictionary will eventually get a color as key, for which it has no amount/color pairs (because some bags don't contain other bags).

And then our bagCount should be correct and we can return that.

And that's basically it.
