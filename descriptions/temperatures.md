# Temperatures

In this exercise, you have to analyze records of temperature to find the closest to zero.

![Sample temperatures](img/temp_fr.png "Here, -1 is the closest to 0.")

Write a program that prints the temperature closest to 0 among input data.

## Input

* **Line 1**: N, the number of temperatures to analyse
* **Line 2**: The N temperatures expressed as integers ranging from _-273 to 5526_

## Output

* Display 0 (zero) if no temperature is provided
* Otherwise, display the temperature closest to 0,
    * knowing that if two numbers are equally close to zero,
    * positive integer has to be considered closest to zero
        * (for instance, if the temperatures are -5 to 5, then display 5)

## Constraints

* 0 ≤ N < 10000

## Example

    Input

        5
        1 -2 -8 4 5

    Output

        1

## Conditions

* Available RAM: 512MB
* Timeout: 1 seconds
* The program has to read inputs from standard input
* The program has to write the solution to standard output
* The program must run in the test environment