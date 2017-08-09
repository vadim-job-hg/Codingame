# https://www.codingame.com/ide/puzzle/power-of-thor-episode-1
import sys
import math
light_x, light_y, initial_tx, initial_ty = [int(i) for i in raw_input().split()]
current_x, current_y = initial_tx, initial_ty
while True:
    remaining_turns = int(raw_input())  # The remaining amount of turns Thor can move. Do not remove this line.
    move_string = ""
    if current_y<light_y:
        move_string = "S"
        current_y = current_y + 1
    elif current_y>light_y:
        move_string = "N"
        current_y = current_y - 1
    if current_x<light_x:
        move_string = move_string + "E"
        current_x = current_x + 1
    elif current_x>light_x:
        move_string = move_string + "W"
        current_x = current_x - 1
    # A single line providing the move to be made: N NE E SE S SW W or NW
    print(move_string)

