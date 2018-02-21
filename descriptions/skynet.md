# Skynet - The Chasm

Los Angeles, 2029. The earth is prey to an unending battle pitting humans against machines controlled by Skynet, the all-powerful self-aware artificial intelligence program. The Résistance is the sole surviving group of humans having survived the nuclear holocaust.

All direct assaults, tirelessly mounted against the machines' headquarters, seem only to provide temporary results and cripple your fighting force. You need to find a way to eradicate the problem at its source. Sheltered by the ruined city's underground structures, the best programmers left alive have developed a **virus capable of reading and modifying the machines' source code** enabling them to gain a certain amount of control over the deadly robots. But getting close enough to them is another story.

Heavily armored and fortified, Skynet's Central Core Installation is completely inacessible to any human being. The Resistance has decided to hijack some Moto-Terminators in order to contaminate them and send them back to Skynet's headquarters with low power reserves. As soon as a motorbike connects to the system to recharge, the virus will spread across the entire network, dealing a swift and fatal blow to Skynet...

We have detected a prime target for initial infection, a Moto-Terminator on the hunt for humans. A brave soldier managed at the cost of his life to inject a prototype of the virus into the machine, granting us limited control over it for a short period of time.

**At the end of a nearby bridge is a suspended platform surrounded by a deep chasm. The goal is to send the bike onto the platform, trapping it for us to pick up.**

The success of this mission is **crucial** for us, we will be able to write a new version of our virus capable of directing several tainted Moto-Terminators back to base at once, maximizing our chance of victory.

## The Program

![Terminator Bike](img/terminator_bike.png 'Terminator Bike')

The bike moves in a straight line (**X** axis) and can jump. Each turn, it moves forward a number of spaces equal to its speed. For example, if X = 1 and speed = 3, X will be 4 at the end of the turn. The bike can start with any speed, including being at a stop.

Our ingeneers have integrated into the virus an SSH tunnel protocol making it possible to send a few simple commands to the Moto-Terminators.

* Upon connection, you will receive the lengths of the road before the gap, the length of the gap and the length of the landing platform.
* After every communication, you will receive the current speed and position on the road of the motorbike.
* The virus prototype accepts four simple commands : SPEED, SLOW, JUMP, WAIT to respectively accelerate, slow down, jump or keep going.
* The mission is a success if the bike comes at a stop on the landing platform.
* You fail if the bike falls.
* You fail if the bike did not get to the platform after 50 turns.

This problem is quite simple. As quickly as possible, reach the minimum speed to jump the gap and you’ll make sure to succeed all the validation tests!

    The program must first read the initialization data from standard input. Then, **within an infinite loop**, read the data from the standard input related to the bike's current state and provide to the standard output the next instruction.

    **Don’t forget to run all the tests** by modifying the value of the “test” variable (1, 2, 3, 4, 5, 6) in the “Test script” window

    **The tests provided are similar to the validation tests used to compute the final score but remain different.**

## Initialization Input:

* **Line 1**: **R** the length of the road before the gap.
* **Line 2**: **G** the length of the gap.
* **Line 3**: **L** the length of the landing platform.

## Input/Turn

* **Line 1**: **S** the motorbike's speed.
* **Line 2**: **X** the position on the road of the motorbike.

## Output/Turn

A single line containing one of 4 keywords:

* _SPEED, SLOW, JUMP, WAIT_.

## Constraints

The initial position of the motorbike is always **X**=0.

* 0 ≤ S < 50
* 0 ≤ X < 100
* 1 ≤ R ≤ 100
* 1 ≤ G ≤ 100
​* 1 ≤ L ≤ 100
​​
Response time for one game turn _≤ 150ms_

## Example

The motorbike starts with a speed of 2, the bridge is of length 4, the gap is of length 2 and the landing platform is of length 5.

    Initialization input (outside the loop)

        4   (R)
        2   (G)
        5   (L)

    No output expected

![Skynet Map #1](img/Skynet1.jpg 'Skynet Map #1')

    Input for turn 1

        2   (S)
        0   (X)

    Output for turn 1

        SPEED

![Skynet Map #2](img/Skynet1_2.jpg 'Skynet Map #2')

_Accelerate to have enough momentum to jump the gap_

    Input for turn 2

        3   (S)
        3   (X)

    Output for turn 2

        JUMP

![Skynet Map #3](img/Skynet1_3.jpg 'Skynet Map #3')

_The bike moved forward 3 spaces. The next space is part of the gap, jump now_

    Input for turn 3

        3   (S)
        6   (X)

    Output for turn 3

        SLOW

![Skynet Map #4](img/Skynet1_4.jpg 'Skynet Map #4')

_The bike jump 3 spaces ahead. Stop the bike by slowing down_
_keep slowing down with SLOW until the motorbike comes to a complete stop..._