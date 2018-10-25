#Genome Sequence

You are working as a computer scientist in a laboratory seeking to sequence the genome. A DNA sequence is represented by a character string _(of  A, C, T and G)_ such as _GATTACA_.

The problem is that biologists are only able to extract sub-sequences of the complete sequence. Your role is to combine these partial sub-sequences to recover the original sequence.
​
So if, for example, you have three sub-sequences _AGATTA, GATTACA, and TACAGA_ you should be able to find the sequence _AGATTACAGA_ which has the property of containing all of these.

Note that in this example, there are other sequences which contain all of the sub-sequences such as _TACAGATTACAGATTA_. However, we prefer the former because it is shorter (10 characters instead of 16).
​
In this exercise you are asked to calculate the length of the shortest sequence that contains the N sub-sequences of the input data.
There may be several sequences of the same minimum length and which fit the requirement. We are not asking you to list these, but only to return their length.

Note that there is always a solution. One can indeed simply concatenate all the sub-sequences to obtain a valid sequence. But by nesting (even partially) the sub-sequences, it is generally possible to obtain a shorter sequence, as shown in the examples.

## Input

* **Line 1**: The number N
* **N Following lines**: one sub-sequence by line, represented by a string of characters from A, C, T and G. Each sub-sequence ranges from 1 to maximum 10 characters long.

## Output

The length of the shortest sequence containing all the sub-sequences.

## Constraints

* 0 < N < 6

## Examples

    Input

        2
        AAC
        CCTT

    Output

        6

    Input

        3
        AGATTA
        GATTACA
        TACAGA

    Output

        10
        
    Input

        3
        TT
        AA
        ACT

    Output

        5

## Conditions

* Available RAM : 512MB
* Timeout: 1 seconds
* The program has to read inputs from standard input
* The program has to write the solution to standard output
* The program must run in the test environment
