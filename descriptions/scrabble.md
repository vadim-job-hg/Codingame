#Scrabble

When playing Scrabble©, each player draws 7 letters and must find a word that scores the most points using these letters.

A player doesn't necessarily have to make a 7-letter word; the word can be shorter. The only constraint is that the word must be made using the 7 letters which the player has drawn.

_For example, with the letters etaenhs, some possible words are: ethane, hates, sane, ant._

## Letter Scoring

In Scrabble©, each letter is weighted with a score depending on how difficult it is to place that letter in a word. You will see below a table showing the points corresponding to each letter:

### Letters Points

* **1**: e, a, i, o, n, r, t, l, s, u
* **2**: d, g
* **3**: b, c, m, p
* **4**: f, h, v, w, y
* **5**: k
* **8**: j, x
* **10**: q, z

_The word banjo earns 3 + 1 + 1 + 8 + 1 = 14 points._

A dictionary of authorized words is provided as input for the program. The program must find the word in the dictionary which wins the most points for the seven given letters. If two words win the same number of points, then the word which appears first in the order of the given dictionary should be chosen.

All words will only be composed of alphabetical characters in lower case. There will always be at least one possible word.
 
## Input

* **Line 1**: The number N of words in the dictionary
* **N following lines**: The words in the dictionary. One word per line.
* **Last line**: The 7 letters available.

## Output

The word that scores the most points using the available letters (1 to 7 letters). The word must belong to the dictionnary. There is always a solution.
 
## Constraints

* 0 < N < 100000
* Words in the dictionary have a maximum length of 30 characters.
 
## Example

    Input

        5
        because
        first
        these
        could
        which
        hicquwh

    Output

        which

## Conditions

* Available RAM : 512MB
* Timeout: 1 seconds
* The program has to read inputs from standard input
* The program has to write the solution to standard output
* The program must run in the test environment
