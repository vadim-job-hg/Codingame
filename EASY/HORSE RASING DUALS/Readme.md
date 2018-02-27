# Horse Dual
Casablanca’s hippodrome is organizing a new type of horse racing: duals. During a dual, only two horses will participate in the race.

In order for the race to be interesting, it’s necessary to try to select two horses with similar strength.

Write a program which, using a given number of strengths, identifies the two closest strengths and shows their difference with a positive integer.

## Input

* **Line 1**: Number N of horses
* **The N following lines**: the strength P<sub>i</sub> of each horse. P<sub>i</sub> is an integer.

## Output

The difference ``D`` between the two closest strengths. ``D`` is a positive integer.

## Constraints

* 1 < N  < 100000
* 0 < P<sub>i</sub> ≤ 10000000

## Example

    Input

        3
        5
        8
        9

    Output

        1

## Conditions

* Available RAM: 512MB
* Timeout: 1 seconds
* The program has to read inputs from standard input
* The program has to write the solution to standard output
* The program must run in the test environment