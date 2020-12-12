# Retrospective #

The author of AoC sure does seem to hold the manhattan distance dear to his heart...

But hey, who am I to complain, I wrote a function for it and placed it in the toolbox.
This problem was the first one this year that I've gotten to use a function in the toolbox, so hey, I'm not complaining. :D

## 12a ##

This problem was fairly straight-forward. The only addition from previous years was that in this case, the orientation didn't need to change for the ship to move in a specific direction.

There are concepts of ships that has the propellers mounted in nacelles on "fins", and the fins in turn mounted on a swivel, so that the ship can just rotate the fins, and off it goes in that direction, so this is not unheard of. Of course, the hull of a ship is usually designed to move forward efficiently, which leaves little room for efficiency in the other directions, but then again, no one would be crazy enough to use that feature for anything but docking maneuvers at port, right? Riiiiight?

I mean, we're not navigating across the sea doing maneuvers like that... oh, we are... well... shit.

## 12b ##

Before solving 12a, and gaining access to the problem description for 12b, I told my [colleague](www.henkla.se/) that I bet that we'd *"misinterpreted"* the instructions in 12a, and that the ship actually turned when instructing it to go in a specific direction (N, E, S, W).

I was correct in anticipating that we'd *"misinterpreted"* the functionality, but was way off on what we'd gotten wrong.

So, it appears that the guidance computer has a single waypoint set, somewhere relative to the ship, and it stays relative to the ship. If the ship moves 1 unit East, the waypoint will also move 1 unit East (wherever it is in relation to the ship).

Most of the commands (except 'F') manipulate the waypoints position relative to the ship.

'F', on the other hand, is the only way to move the ship, and simply moves the ship to the waypoint the specified amount of times (and since the waypoint is relative to the ship, when the ship has reached the waypoint position, the waypoint position has moved away to a new position).

I.e. if ship is at (0,0) and waypoint is at (1,1), if we move to the waypoint, then the ship position becomes (1,1) and since the waypoint is relative to the ship, it will now be at (2,2).

So what I did was that I calculate the delta between shipX/waypointX and shipY/waypointY, then I move the ship to the waypoint position, and calculate the new waypoint position by grabbing the (new) ship position and addint the deltas to those coords.

For the 'L' and 'R' actions (rotate, in which it is now the waypoint which rotates around the ship) I grabbed a piece of gridlined paper, and put the ship at a point in the center of the paper, at (0,0), and initial state of the waypoint (-1, 10) (i.e. North 1, East 10), and also marked out what point it would end up on if rotating left/right 90 degrees, and also left (or right, doesn't matter) 180 degrees.

From that I observed that if I was turning the waypoint counter-clockwise (left) 90 degrees, and had a positive deltaX, this would be transformed into the negative deltaY and vice-versa
positive deltaY would however turn into positive deltaX, and vice-versa.

For right 90 degrees, positive deltaX turned into positive deltaY (and vice-versa), and positive deltaY turned into negative deltaX.

Note how dx and dy trade places with each other.

I had some trouble getting all this to work, but I just tacked on more and more tests until I narrowed it down to the "rotation" code in moveWaypoint.

Turned out that I wasn't adding the ships position to the deltas, which meant that while the ship may have moved far away from (0, 0), the newly calculated (rotated) waypoint position was always fairly close to (0, 0)...

Fun all around. Also not the most beautiful of code... but hey, I am getting better at writing testable code.

Which for the most part just means that I am getting better at writing functions which takes as parameters all the data the function needs to perform it's calculation.

So simple really...
