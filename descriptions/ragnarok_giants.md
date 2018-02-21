# Thor Vs. Giants

Thor strides bravely into the ultimate battle of the Ragnarök, armed with his hammer, which has regained its powers.

In the forefront, a large number of Fire giants, who are the secular enemies of the gods, have come down to the plains of Vigrid to fight Thor.

Thor is counting on the strength of his hammer’s light bolt of power to beat them, but he is still weak and he can only use his hammer a limited number of times.

## The Program

In the same way as for the previous game, you will move on a map of 40 wide by 18 high. Thor must annihilate all the giants on the map: by striking the ground with his hammer he sends out a bolt of light which wipes out the giants which are nearby.

The number of times you can strike the ground is limited.

* Each turn, you must either specify an action :
    * WAIT Thor does nothing.
    * STRIKE Thor strikes.
    * Or you can move in the same way as in the previous game:

### Possible moves

* **N** (North)
* **NE** (North-East)
* **E** (East)
* **SE** (South-East)
* **S** (South)
* **SW** (South-West)
* **W** (West)
* **NW** (North-West)

Each time Thor strikes, all the giants in a square centered on Thor and of 9 spaces wide are destroyed.

On each turn during the game, once Thor has carried out an action, all the remaining giants on the map move in the direction of Thor (without ever overlapping each other).

**You win** when there are no more giants left on the map.

#### You lose:
* if a giant moves on top of Thor
* if there are giants remaining on the map and Thor doesn't have any hammer strikes left.
* if Thor moves off the map
* if the program exceeds the maximum number of authorized turns, which is fixed at 200

The program must first read the initialization data from standard input. Then, within an infinite loop, read the data from the standard input related to Thor's current state and provide to the standard output Thor's movement instructions.

Do not hesitate to use the Previous/Next question buttons to reuse your code from the previous question (copy/paste).

Don’t forget to run all the tests by modifying the value of the “test” variable _(1, 2, 3, 4)_ in the “Test script” window

The tests provided are similar to the validation tests used to compute the final score but remain different.

## Initialization Input

* **Line 1**: 2 integers ``TX TY``, initial position of thor

## Input / Game Turn

* **Line 1**: 2 integers ``H N``.
    * ``H`` indicates the remaining number of hammer strikes.
    * ``N`` the number of giants which are still present on the map.on
* **N following lines**: the positions ``X Y`` of the giants on the map.

## Output / Game Turn

A single line which indicates the movement or action to be carried out: ``WAIT STRIKE N NE E SE S SW W or NW``
 
## Constraints

* 0 ≤ TX < 40
* 0 ≤ TY < 18
* 0 < H ≤ 100
* 0 < N ≤ 100
* 0 ≤ X < 40
* 0 ≤ Y < 18
* Response time for each turn ≤ 100ms

## Example

* **Initialization**
    * input _(out of the infinite loop)_
        * ``3 6``
            * Thor’s starting position on the map is (3, 6)
    * No output is expected
        * A single giant is on position (3, 8)
* **Turn 1** _(start of the infinite loop)_:
    * input:
        * ``10 1``
            * _Thor has 10 strikes left_
            * _There is 1 giant left on the map_
        * ``3 8``
            * _The giant is in position (3,8)_
    * output:
        * ``WAIT``
            * _Thor does nothing_
* **Turn 2**
    * input:
        * ``10 1``
            * _Thor has 10 strikes left_
            * _There is 1 giant left on the map_
        * ``3 7``
            * _The giant is in position (3,7)_
    * output:
        * ``STRIKE``
            * _Thor strikes and sends out a bolt of light._
* **Thor has won: the giant has been annihilated!**
