# Retrospective #

I'm really off my game. I guess sleep deprivation is the primary reason, and stressing over work being a close second.

So, today I made some really stupid and in retrospect really obvious mistakes, that took a bit of debugging to root out.

The problems were sortof fun, although I am getting flashbacks from an earlier year, possibly 2018... there was one year that was filled with "hey let's make a little game"-type of problems.

Perhaps it was using intcode in 2019... I can't remember.


## 11a ##

So, this problem revolves around iteratively transforming a playing field from one state to another.

If you are familiar with web development, then if I say *"building a shadow-DOM"* may help get the idea across.

The state of each cell in the *"evolved"* playing field, depends on the state of that cell's adjacent cells in the current playing field.

In the A problem, I managed to bungle up the if-statements governing what cells would transform how, so for a while there it just inverted the playing field, toggling between 'L' and '#'.

Explained my woes to my colleague, pasted the relevant part of the code, and immediately saw what the problem was...

In short, I tried to do too many comparisons in one statement, and had an else case to catch everything else. And it should not have caught everything else...

Here I would have benefitted from actually doing what I said I'd do a couple of days ago: implementation plan light, through comments in the code...

But I haven't and my code suffered for it.


## 11b ##

I couldn't even figure out what the hell the new updated adjacency rule meant. I would probably have gotten it after a few more re-reads, but my colleague came to the rescue again, and re-stated the problem in a way I could understand.

So, instead of just being concerned with the state of the 8 surrounding cells, we should now take into consideration the first chair in line of sight in all 8 directions.

The test data didn't make sense until I got the re-stated explanation, whereupon it immediately made perfect sense.

Again I was sloppy, this time trying to exit loops, which didn't exactly go as planned, so even though I tried to check and account for going out of bounds of the playing field, my own logic allowed the code to continue anyway...

This, however, made me break my code into smaller pieces (functions) so that I could more easily add increasingly more specific tests (they are still in b.py if anyone is interested).

The best thing I can say about today is that I really like the template and test-framework I have set up. It makes debugging so much easier (if/when I actually make code that is testable in isolation).
