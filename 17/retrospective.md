# Retrospective #

Today's problem can be described like this: _"[Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life)... in 3D!"_

The rules were tweaked a bit, we only ran the simulation for 6 cycles, but in principle it is the same thing.

The more I worked on the solution, the more things I realize about the problem and how it ties to the solution.


## 17a ##

My initial thought for representing the world, which allegedly was infinite in all three dimensions (good thing we didn't need to test that since our 6 iterations will never get us very far), was to have a dictionary, using tuples of `(x, y, z)` as the key, and the number of active neighboring cubes as the value.

This dictionary would be our _"current state"_.

But I also quickly realized that since I once again (as in a previous problem this year) needed to make a clone of the current state, and based on the values in the current state, modify the clone (henceforth _"next state"_).

This meant that I also needed to somehow keep track of what cubes are currently active.

At this point it didn't dawn on me that I actually only needed to keep track of active cubes neighboring ACTIVE cubes... (don't worry, I will get back to this in a bit, let me just flesh out the progression which eventually lead to the solution and the epiphany)

So, my next thought was that _"OK, I'll create a Cube-class, which will store it's own state (active/inactive) as well as it's own coordinates."_ This is duplication of data, as the coordinates will now exist both as the key in the dictionary, which points to the Cube-object, which also holds the coordinates.

But having the coordinates within the object allows us to create a method `neighbours()` which return a sequence of (x, y, z) tuples, all of which are at most one step away from the cube-object's own coordinates.

Granted, this method could have taken the coordinates as a parameter, but I didn't think of that, mmmmkay?

I then also proceeded to create a `count_active_neighbours(worldState)` method, which uses the above `neighbours()` to generate a list of coordinates, and for each such tuple, it checks if that tuple exist as a key in the current state (delivered as the argument _"worldState"_), and if the key exists (i.e. it is tied to a Cube object, ask that object if it `is_active()`

I felt pretty smart about myself.

Then main logic, then, is a loop, iterating as many cycles as was specified (6), and for each iteration we: (this will be a mile-high short description, more to follow below)

1. make a copy of currentState, call it newState.
2. make a list of coordinates which we need to check. This list should contain the coordinates of all active cubes in currentState, as well as all the neighbouring coordinates of the active cubes in currentState
3. then, for each coordinate in this set of coordinates:
4. check if the coordinate is documented in currentState:
    1. if coordinate exists in currentState, check if the Cube in that place is active:
        1. if Cube at coordinate is active , check how many active neighbours it has, one rule says that if there are less than 2 active neighbours, or more than 3, then this Cube should become inactive (in the newState, not in our currentState), otherwise:
        2. if Cube at coordinate is inactive, check how many active neighbours it has, another rule says that if there are exactly three active neighbours around a Cube, and it is inactive, then it should be activated (in newState). If there are more coordinates to check, jump back to #3 and grab a new coordinate to evaluate, otherwise goto #5.
    2. if coordinate does not exist in currentState that means that it is by default an inactive Cube in that coordinate, so we should check if this coordinate has exactly three neighboring coordinates with active Cubes, and if it has, then we should add an active Cube in this position to newState. If there are more coordinates to check, jump back to #3 and grab a new coordinate to evaluate, otherwise goto #5.
5. overwrite currentState with newState, begin a new iteration/cycle.

This is all convoluted horseshit. (It is also the code currently in the repository, as of commit 24a63706c06163c5ac90051fcfb25ff631c0d2ed...)

You see, while I was debugging the shit out of one bug or another I had an epiphany: **Only the active cubes matter.**

So any inactive cube, we should purge relentlessly from our newState. The ONLY coordinates/Cube-objects that should be present in newState, are active Cubes.

Which means that we should, in theory, be able to go back to my first idea: A dictionary with (x, y, z) as key, and active neighbour count as value.

**The very existence of a key/value combination in the dictionary IS an indication that the cube in this coordinate (key) is active, otherwise we wouldn't have bothered with documenting it.**

At this point, the only thing the Cube-class gives us (since we can now rely on existence of key/value pair in the dictionary for state) is the functionality of calculating the number of active cubes neighbouring it, and for that it already needs the state itself anyway.

So this could be a standalone function `count_active_neighbours_for(coordinate, worldState)`

Remember above, how I said that #2 in the primary logic was to make a list (set) of coordinates for all active cubes, and their neighbours? This is the only place where we ever need to think about anything other than active cubes. (Because one of those coordinates may have the right number of active neighbours to become active itself.)


So, a little pseudo-code:

    cycleCount = 6;
    currentState = bootstrapWorld(inputData);

    for (i = 0; i < cycleCount; i++) {

        newState = currentState.clone();

        coordsToEvaluate = set();
        for (coord in currentState.keys()) {
            coordsToEvaluate.add(coord);
            for (neighbourCoord in neighbours(coord)) {
                coordsToEvaluate.add(neighbourCoord);
            }
        }

        for (coord in coordsToEvaluate) {
            if (coord in currentState.keys()) {
                // active cube
                activeNeighbourCount = getActiveNeightboursFor(coord, currentState);
                if (activeNeighbourCount < 2 || activeNeighbourCount > 3) {
                    newState.remove(coord);
                }
            } else {
                // inactive cube
                if (getActiveNeightboursFor(coord, currentState) == 3) {
                    newState.add(coord);
                }
            }
        }

        currentState = newState;
    }

    return currentState.length();

You know what? We don't even need to know the number of active neighbours to a specific coordinate, which means that we don't even need a dictionary. A sequence (set) will do just fine.
I am still realizing things about this problem, right here, right now. Very nice! :) (Unless of course I am forgetting something crucial, the above is after all just untested pseudo-code...)

One thing I've learned today, about Python, is `copy.deepcopy`. Consider the above case, a dict with instantiated objects as values. We make a copy of this dictionary, and if we just did `newState = currentState.copy()` (i.e. using the dictionaries built-in `.copy()` method), our new dictionary would have references to our objects in the old dictionary. If we altered the internal state of an object found in the copy, then the object in the original dictionary would be updated as well (since they are the same object, just with references from two different locations).

`copy.deepcopy()`, however, is very thorough. Any complex data (like objects) will be instantiated with the same values, so while they will look and act identical, they now occupy different parts of memory, and are independent of each other (between the original dict and the copy). **VERY** nice!

Now I am of course very tempted to rewrite 17a to conform with the above pseudo-code..., but first:


## 17b ##

My speculation over lunch was that there would be another _"increase difficulty by increasing iteration length"_ (say, 30 million iterations instead of 6, like the other day).

But instead, we got a fourth dimension added!

The only thing I needed to do was copying my 17a code, find any place speaking about (x, y, z), and replace that with (x, y, z, w), and any place I had a triply nested loop (iterating over combinations of x, y, and z) I now just added another outer loop for w as well.

Fuck ugly, slow, probably massively inefficient, but my RPi didn't choke on the problem, and delivered the correct result. Woop woop.
