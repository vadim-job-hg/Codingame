# https://www.codingame.com/ide/puzzle/the-descent
import sys
import math

# The while loop represents the game.
# Each iteration represents a turn of the game
# where you are given inputs (the heights of the mountains)
# and where you have to print an output (the index of the mountain to fire on)
# The inputs you are given are automatically updated according to your last actions.


# game loop
while True:
    mountain_max = 0
    index_max = 0
    for i in range(8):
        mountain_h = int(input())  # represents the height of one mountain.
        if mountain_max<mountain_h:
            mountain_max = mountain_h
            index_max = i
    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)
    print('INDEX -'+str(index_max), file=sys.stderr)
    print('MAX - '+str(mountain_max), file=sys.stderr)
    # The index of the mountain to fire on.
    print(str(index_max))

