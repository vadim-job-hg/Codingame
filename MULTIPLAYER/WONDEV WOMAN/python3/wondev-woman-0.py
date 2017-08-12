# https://www.codingame.com/ide/puzzle/wondev-woman
import sys
import math

REVERSE = {
    'N': 'S',
    'S': 'N',
    'E': 'W',
    'W': 'E',
    'NE': 'SW',
    'NW': 'SE',
    'SE': 'NW',
    'SW': 'NE'
}


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
def get_back_action(atype, index, dir_1, dir_2):
    return "{0} {1} {2} {3}".format(atype, index, REVERSE[dir_1], REVERSE[dir_2])


first_action = second_action = None
k = 2
size = int(input())
units_per_player = int(input())
# game loop
while True:
    map = []
    for i in range(size):
        row = input()
        map.append(row)
        # print("i: {0} row: {1}".format(i,row), file=sys.stderr)
    for i in range(units_per_player):
        unit_x, unit_y = [int(j) for j in input().split()]
        # print("unit_x: {0} unit_y: {1}".format(unit_x,unit_y), file=sys.stderr)
    for i in range(units_per_player):
        other_x, other_y = [int(j) for j in input().split()]
        # print("other_x: {0} other_y: {1}".format(other_x,other_y), file=sys.stderr)
    legal_actions = int(input())
    # print("legal_actions {0}".format(legal_actions), file=sys.stderr)
    for i in range(legal_actions):
        atype, index, dir_1, dir_2 = input().split()
        if (first_action is None):
            first_action = "{0} {1} {2} {3}".format(atype, index, dir_1, REVERSE[dir_1])
            second_action = get_back_action(atype, index, REVERSE[REVERSE[dir_1]], REVERSE[dir_1])
        # print("i {0} {1} {2} {3} {4}".format(i, atype, index, dir_1, dir_2), file=sys.stderr)
        index = int(index)

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)
    # print(k, k%2, file=sys.stderr)
    if k % 2 == 0:
        print(first_action)
    else:
        print(second_action)
    k = k + 1

