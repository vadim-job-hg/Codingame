# The Descent

_"**Captain's log, stardate 1567.9**. We are entering the Deneb system two days after receiving a distress call issuing from the unexplored planet XIV of this system. Our mission is to bring aid to whomever is in need of our help on this planet."_

_"**Captain's log, supplemental**. While reaching the planet, our rescue ship was drawn to a point on the surface by an invisible force that we have yet to understand. Despite all efforts, the ship continues its downward course and we are at great risk of colliding with the mountains that tower below us."_

_"**Captain's log, supplemental**. In a final attempt, Scotty was able to re-engineer the phase cannons so that they can now destroy the mountains from their foundations. This gives us hope of landing safely on the planet. Unfortunately, the cannons must be used sparingly as they are slow to recharge. **We are now looking for a crew member able to program the firing rate of the phase cannons** to get us out safely from what clearly appears to be a trap designed to destroy us."_

## The Program

Your mission is to program the cannons so that they destroy the mountains **before your starship collides with them**.

There are **8** mountains. The starship **circles above all the mountains**, going first from left to right, then from right to left, and so on and so forth. With each complete pass, the starship **descends one kilometer** as it is being drawn to the surface by an unknown force.

A complete pass is done in 8 game turns.

You can **only fire once per pass** on the mountain located **directly below the starship**. Firing on a mountain base **will only destroy part of it** and it will sink a random number of kilometers.

* For a landing to be successful, all the mountains must be destroyed completely.
* You fail if the starship collides with a mountain.
* Firing on highest mountains first, ensures a safe landing.

    **Within an infinite loop**, read the data from the input channel related to the current state of the landing and send to the output channel the starship firing instructions.

    **Don’t forget to run all the tests** by modifying the input file

## Input Per Game Turn

* **Line 1**: 2 integers: SX SY
  * SX is the horizontal coordinate or your starship (in kilometers). It goes from 0 (left of the screen, above first mountain) to ``7`` (right of the screen above last mountain)
  * SY is the current altitude of your ship (in kilometers). It goes down from ``10`` (top of the screen) to ``1`` (just above ground).
* **Next 8 lines**: One integer MH per line. It represents the height of one mountain, from 9 to 0 (mountain destroyed). Mountains' heights are provided from left to right.

## Output Per Game Turn

* A single line with either: ``FIRE`` (ship is firing its phase cannons) or ``HOLD`` (ship is not firing)

## Constraints

* 0 ≤ SX ≤ 7
* 0 < SY ≤ 10
* 0 ≤ MH ≤ 9
* Response time per turn ≤ **100ms**

## Example

#### Turn #1

    Input

        0 10
        5
        4
        8
        4
        1
        0
        2
        9

    Output

        FIRE

_User starts at position (0,10) and shoots._

#### Turn #2

    Input

        1 10
        2
        4
        8
        4
        1
        0
        2
        9

    Output

        HOLD

_User did 3 damage to the first mountain and is holding fire._