# Stock Exchange Losses

![Stock Exchange Losses](img/stock_exchange_losses.jpg 'Stock Exchange Losses')

A finance company is carrying out a study on the worst stock investments and would like to acquire a program to do so. The program must be able to analyze a chronological series of stock values in order to show the largest loss that it is possible to make by buying a share at a given time _t0_ and by selling it at a later date _t1_. The loss will be expressed as the difference in value between _t0_ and _t1_. If there is no loss, the loss will be worth _0_.

## Input

* **Line 1**: the number n of stock values available.
* **Line 2**: the stock values arranged in order, from the date of their introduction on the stock market v1 until the last known value vn. The values are integers.

## Output

The maximal loss _p_, expressed negatively if there is a loss, otherwise _0_.
 
## Constraints

* 0 < n < 100000
* 0 < v < 231

## Examples

### Example 1

    Input

        6
        3 2 4 2 1 5

    Output

        -3

![Perte 1](img/perte1.png 'Perte 1')

### Example 2

    Input

        6
        5 3 4 2 3 1

    Output

        -4

![Perte 2](img/perte2.png 'Perte 2')

### Example 3

    Input

        5
        1 2 4 4 5

    Output

        0

![Profit](img/profit.png 'Profit')

## Conditions

* Available RAM: 512MB
* Timeout: 1 seconds
* The program has to read inputs from standard input
* The program has to write the solution to standard output
* The program must run in the test environment