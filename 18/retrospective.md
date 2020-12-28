# Retrospective #

Interesting problem. While most (?all?) programming languages in the world will attempt to guide you clear of messing up PEMDAS, this problem actively seeks to do just that.

In 18a parens are still first, exponents are not part of the problem, nor is division or subtraction, but multiplication and addition are considered of equal importance, so just parse them from left to right...

For 18b addition is more important than multiplication.

In either case, our first order of business is to figure out what the sub-expressions within the parens amount to.

One very nice thing about math, (unlike the first ever Advent of Code problem ([2015 1a](https://adventofcode.com/2015/day/1))) is that the parens MUST always be balanced.

Which means that there WILL be a closing paren for every opening paren. And they can't be out of sequence (you can't have a closing paren BEFORE an opening paren).

So if we just find the right-most opening paren, and the left-most closing parent at least one character beyond where we found the right-most opening paren, we are guaranteed to have the inner-most sub-expression (and we need to get to the very bottom (inner-most) and work our way outwards, to resolve all potential expressions.)

If we can get that working, and calculate the answer to whatever is in that sub-expression, and then REPLACE that entire sub-expression, including the enclosing paren-pair, with that calculated answer, then we can just do a `while "(" in inputString: ...`

In 18a our code can then simply tokenize all the terms by splitting on white-space, and pop elements off from left to right, one at a time.
Pretty sleek if you ask me.

For 18b, we had to prioritize addition over multiplication, and the least complex way I figured was to reuse known-and-proven methods, so I give you a variation of `while "(" in inputLine: ...`: the `while "+" in inputLine: ...` (really high-tech stuff here...)

Once we have consumed all additions, and replaced those expressions with values, the only things left should be numbers (either from the initial input, or calculated via additions or paren-subexpressions) and multiplication signs. So let's just multiply and see what happens.
