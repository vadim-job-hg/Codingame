# Roller Coaster

You have recently been assigned to a new amusement park’s center of analysis and supervision. Your mission is to estimate each day what the earnings will be for each ride that day.

You start by looking at the roller coaster.

![Roller Coaster](img/roller.png 'Roller Coaster')

You notice that people like the roller coaster so much that as soon as they have finished a ride, they cannot help but go back for another one.

* People queue up in front of the attraction
* They can either be alone or in a group. When groups are in the queue, they necessarily want to ride together, without being separated.
* People never overtake each other in the queue.
* When there isn’t enough space in the attraction for the next group in the queue, the ride starts (so it is not always full).
* As soon as the ride is finished, the groups that come out, go back into the queue in the same order.

* The attraction contains a limited number **L** of places.
* The attraction can only function **C** number of times per day.
* The queue contains a number **N** of groups.
* Each group contains a number **P<lower>i</lower>** of people.
* Each person spends **1 dirham** per ride.

**Example** with L=3, C=3 and 4 groups (N=4) of the following sizes [3,1,1,2]

* **Ride 1**: For the first roller coaster ride, only the first group can get on and takes all the places. At the end of the ride, this group returns to the back of the queue that now looks as follows [1,1,2,3].
    * _Earnings of the ride_: 3 dirhams.
* **Ride 2**: On the second ride, the following two single-person groups can get on, leaving one place empty (the group of 2 people that follows cannot be separated) At the end of the ride, they return to the back of the queue: [2,3,1,1]
    * _Earnings of the ride_: 2 dirhams.
* **Ride 3**: For the last ride (C=3), only the group of 2 people can get on, leaving one place empty.
    * _Earnings of the ride_: 2 dirhams.

**Total earnings**: 3+2+2 = 7 dirhams

## Input

* **Line 1**: The integers **L**, **C** and **N** separated by a space.
* **N following lines**: Each line contains an integer **P<lower>i</lower>** representing the number of people in a group. The lines are ordered in the same way as the queue. (The first lines correspond to the first groups that can get on the ride).correspondant au nombre de personnes dans un groupe.

## Outut

An integer representing the number of dirhams earned at the end of the day on the roller coaster (after **C** roller coaster rides)

## Constraints

* **P<lower>i</lower>** ≤ **L**
* 1 ≤ **L** ≤ 109
* 1 ≤ **C** ≤ 108
* 1 ≤ **N** ≤ 10000
* 1 ≤ **P** ≤ 107

## Examples

#### Example #1

    Input

        3 3 4
        3
        1
        1
        2

    Output

        7

#### Example #2

    Input

        5 3 4
        2
        3
        5
        4

    Output

        14

#### Example #3

    Input

        10 100 1
        1

    Output

        100

## Conditions

* Available RAM: 512MB
* Timeout: 1 seconds
* The program has to read inputs from standard input
* The program has to write the solution to standard output
* The program must run in the test environment