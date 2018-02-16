# Conway Sequence

            1
           1 1
           2 1
         1 2 1 1
       1 1 1 2 2 1
       3 1 2 2 1 1
           ...

Warning! This sequence can make you ill. The reasoning is simple but unusual: Read a line aloud whilst looking at the line above and you will notice that each line (except the first) makes ​​an inventory of the previous line.

Line 3 shows ``2 1`` because the line 2 contains two ``1``, one after the other.
Line 4 displays ``1 2 1 1`` because the line 3 contains a one ``2`` followed by a one ``1``.
Line 5 displays ``1 1 1 2 2 1`` because the line ``4`` contains a one ``1`` followed by a one ``2`` followed by a two ``1``.

This sequence refers to a technique used to encode ranges in order to compress identical values ​​without losing any information. This type of method is used, amongst others, to compress images.

Your mission is to write a program that will display the line L of this series on the basis of an original number R (R vaut 1 in our example).

## Input

* **Line 1**: The original number R of the sequence.
* **Line 2**: The line L to display. The index of the first line is 1.

## Output

The line L of the sequence. Each element of the sequence is separated by a blank space.

## Constraints

* 0 < R < 100
* 0 < L ≤ 25

## Example

    Input

        1
        6

    Output

        3 1 2 2 1 1

## Conditions

* Available RAM: 512MB
* Timeout: 1 seconds
* The program has to read inputs from standard input
* The program has to write the solution to standard output
* The program must run in the test environment