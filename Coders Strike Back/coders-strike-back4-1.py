# https://www.codingame.com/ide/puzzle/coders-strike-back
import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.


# game loop
while True:
    # next_checkpoint_x: x position of the next check point
    # next_checkpoint_y: y position of the next check point
    # next_checkpoint_dist: distance to the next checkpoint
    # next_checkpoint_angle: angle between your pod orientation and the direction of the next checkpoint
    x, y, next_checkpoint_x, next_checkpoint_y, next_checkpoint_dist, next_checkpoint_angle = [int(i) for i in
                                                                                               input().split()]
    opponent_x, opponent_y = [int(i) for i in input().split()]

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)
    avaliable_boost = True
    trust = 0
    abs_angle = math.fabs(next_checkpoint_angle)
    if avaliable_boost and next_checkpoint_dist > 1000 and abs_angle < 10:
        trust = 'BOOST'
    elif abs_angle < 10:
        trust = str(100)
    elif next_checkpoint_dist > 3000:
        if abs_angle < 90:
            trust = str(100)
        else:
            trust = str(0)
    else:
        if abs_angle > 90:
            trust = str(0)
        else:
            trust = str(int((1 - abs_angle / 180) * 100))

    # You have to output the target position
    # followed by the power (0 <= thrust <= 100)
    # i.e.: "x y thrust"
    print(str(next_checkpoint_x) + " " + str(next_checkpoint_y) + " " + trust)
