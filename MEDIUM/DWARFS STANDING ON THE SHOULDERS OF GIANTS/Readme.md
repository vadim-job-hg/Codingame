# Dwarfs standing on the shoulders of giants

The saying "_Dwarfs standing on the shoulders of giants_" refers to the importance of being able to build upon the work of our predecessors.

When we read texts, we often only get a small glance of this dependence: this person influenced that person. Thereafter, we learn that the second person, in turn influenced a third and so on. In this exercise we’re interested in the chain of influence and more precisely in finding the longest possible chain.
​
We choose to represent each person by a distinct integer. If person #1 has influenced persons #2 and #3 and person #3 has influenced #4 then there is a succession of thoughts between #1, #3 and #4. In this case, it’s the longest succession and the expected result will be 3, since it involves 3 people.

![DG1](img/dg1.png 'DG1')

If we were to complete this example when we learn that person #2 also influenced persons #4 and #5, then the longest succession will still have a length of 3, but there will now be several of them.

![DG2](img/dg2.png 'DG2')

If we now add that person #10 influenced person #11, the result remains 3. However, as soon as we learn that #10 also influenced #1 and #3, then the result becomes 4, since there is now a succession involving 4 people, which is #10, #1, #2, #5.

![DG3](img/dg3.png 'DG3')

It takes time for a thought to influence others. So, we will suppose that it is not possible to have a mutual influence between people, i.e. If A influences B (even indirectly through other people), then B will not influence A (even indirectly). Also, you can not influence yourself.

## Input

* **Line 1**: The number N of relationships of influence.
* **N following lines**: a relationship of influence between two people in the form of X (whitespace) Y, which indicates that X influence Y. The relationships of influence are listed in any order.

## Output

* The number of people involved in the longest succession of influences.

## Constraints

* 0 < N < 10000
* 0 < X,Y < 10000

## Examples

#### Example #1

    Input

        3
        1 2
        1 3
        3 4

    Output

        3

![DG4](img/dg4.png 'DG4')

#### Example #2

    Input

        8
        1 2
        1 3
        3 4
        2 4
        2 5
        10 11
        10 1
        10 3

    Output

        4

![DG5](img/dg5.png 'DG5')

#### Example #3

    Input

        4
        2 3
        8 9
        1 2
        6 3

    Output

        3

## Conditions

* Available RAM: 512MB
* Timeout: 1 seconds
* The program has to read inputs from standard input
* The program has to write the solution to standard output
* The program must run in the test environment