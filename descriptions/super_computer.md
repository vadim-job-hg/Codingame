# Super Computer

In the Computer2000 data center, you are responsible for planning the usage of a supercomputer for scientists.

​Therefore you've decided to organize things a bit by planning everybody’s tasks. The logic is simple: the higher the number of calculations which can be performed, the more people you can satisfy.
Scientists give you the starting day of their calculation and the number of consecutive days they need to reserve the calculator.

## For example:

    Calculation     Starting Day    Duration
    A               2               5
    B               9               7
    C               15              6
    D               9               3

* Calculation A starts on day 2 and ends on day 6
* Calculation B starts on day 9 and ends on day 15
* Calculation starts on day 15 and ends on day 20
* Calculation D starts on day 9 and ends on day 11
* In this example,
    * it’s not possible to carry out all the calculations because the periods for B and C overlap.
    * 3 calculations maximum can be carried out: A, D and C. . 

## Input

* **Line 1**: The number N of calculations
* **The N following lines**: on each line, the starting day J and the duration D of reservation, separated by a blank space.

## Output

The maximum number of calculations that can be carried out.

## Constraints

* 0 < N < 100000
* 0 < J < 1000000
* 0 < D < 1000

## Examples

    Input

        4
        2 5
        9 7
        15 6
        9 3

    Output

        3
        

    Input

        5
        3 5
        9 2
        24 5
        16 9
        11 6

    Output

        4

## Conditions

* Available RAM: 512MB
* Timeout: 1 seconds
* The program has to read inputs from standard input
* The program has to write the solution to standard output
* The program must run in the test environment
