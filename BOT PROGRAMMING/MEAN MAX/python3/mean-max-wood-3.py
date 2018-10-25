import sys
import math


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
# Distance function
def distance(xi, xii, yi, yii):
    sq1 = (xi - xii) * (xi - xii)
    sq2 = (yi - yii) * (yi - yii)
    return math.sqrt(sq1 + sq2)


chosed_x, chosed_y, throttle = 0, 0, 300
# game loop
while True:
    my_score = int(input())
    enemy_score_1 = int(input())
    enemy_score_2 = int(input())
    my_rage = int(input())
    enemy_rage_1 = int(input())
    enemy_rage_2 = int(input())
    unit_count = int(input())
    for i in range(unit_count):
        unit_id, unit_type, player, mass, radius, x, y, vx, vy, extra, extra_2 = input().split()
        unit_id = int(unit_id)
        unit_type = int(unit_type)
        player = int(player)
        mass = float(mass)
        radius = int(radius)
        x = int(x)
        y = int(y)
        vx = int(vx)
        vy = int(vy)
        extra = int(extra)
        extra_2 = int(extra_2)
    if ((chosed_x, chosed_y) != (x, y)):
        throttle = 300
    elif (throttle > 0):
        throttle -= 30
    print("{0} {1} {2}".format(x, y, throttle))
    print("WAIT")
    print("WAIT")
    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)


