# https://www.codingame.com/ide/puzzle/great-escape
import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# w: width of the board
# h: height of the board
# player_count: number of players (2 or 3)
# my_id: id of my player (0 = 1st player, 1 = 2nd player, ...)
w, h, player_count, my_id = [int(i) for i in input().split()]

# game loop
while True:
    for i in range(player_count):
        # x: x-coordinate of the player
        # y: y-coordinate of the player
        # walls_left: number of walls available for the player
        x, y, walls_left = [int(j) for j in input().split()]
    wall_count = int(input())  # number of walls on the board
    for i in range(wall_count):
        # wall_x: x-coordinate of the wall
        # wall_y: y-coordinate of the wall
        # wall_orientation: wall orientation ('H' or 'V')
        wall_x, wall_y, wall_orientation = input().split()
        wall_x = int(wall_x)
        wall_y = int(wall_y)

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)


    # action: LEFT, RIGHT, UP, DOWN or "putX putY putOrientation" to place a wall
    print("RIGHT")