# https://www.codingame.com/ide/puzzle/wondev-woman
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
    for i in range(units_per_player):
        unit_x, unit_y = [int(j) for j in input().split()]
    for i in range(units_per_player):
        other_x, other_y = [int(j) for j in input().split()]
    legal_actions = int(input())
    for i in range(legal_actions):
        atype, index, dir_1, dir_2 = input().split()
        if (first_action is None):
            first_action = "{0} {1} {2} {3}".format(atype, index, dir_1, REVERSE[dir_1])
            second_action = get_back_action(atype, index, REVERSE[REVERSE[dir_1]], REVERSE[dir_1])
        index = int(index)

    if k % 2 == 0:
        print(first_action)
    else:
        print(second_action)
    k = k + 1

