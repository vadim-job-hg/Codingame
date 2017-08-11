import sys
import math

MAX_HEIGHT = 4


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
def obj(x, y, d):
    return {'x': x, 'y': y, 'd': d}


def array_area(x, y):
    return [
        obj(x - 1, y, 'W'),
        obj(x - 1, y - 1, 'NW'),
        obj(x, y - 1, 'N'),
        obj(x + 1, y - 1, 'NE'),
        obj(x + 1, y, 'E'),
        obj(x + 1, y + 1, 'SE'),
        obj(x, y + 1, 'S'),
        obj(x - 1, y + 1, 'SW')
    ]


class Area:
    size = None
    map = []

    def __init__(self):
        self.size = int(input())

    def b_map(self):
        self.map = []
        for i in range(self.size):
            self.map.append(list(input()))

    def get_value(self, x, y):
        return self.map[y][x]

class Player():
    x = y = 0

    def scan_pos(self):
        self.x, self.y = [int(j) for j in input().split()]

    def get_legal_actions(self):
        legal_actions = int(input())
        for i in range(legal_actions):
            atype, index, dir_1, dir_2 = input().split()
            index = int(index)

    def run(self, area, enemy):
        current_height = int(area.get_value(self.x, self.y))
        move_to, new_height = self.get_best_coors_to_move(area, current_height, self.x, self.y, enemy)
        build_to, new_height2 = self.get_best_coors_to_build(area, new_height, move_to['x'], move_to['y'], enemy)
        # move_to = self.get_best_coors_to_build(area, current_height)
        print("MOVE&BUILD 0 {0} {1}".format(move_to['d'], build_to['d']))

    def get_best_coors_to_move(self, area, current_height, x, y, enemy):
        best_coors = None
        best_val = -1
        for coors in array_area(x, y):
            try:
                if coors['x'] >= 0 and coors['y'] >= 0 and not (enemy.y == coors['y'] and enemy.x == coors['x']):
                    value = area.get_value(coors['x'], coors['y'])
                    if value == '.':
                        continue
                    # todo: enemy not here
                    elif best_val < int(value) and int(value) <= current_height + 1 and int(value) < MAX_HEIGHT:
                        best_val, best_coors = int(value), coors.copy()
                        # print("value {0}".format(value), file=sys.stderr)
            except Exception as e:
                continue
        return best_coors, best_val

    def get_best_coors_to_build(self, area, current_height, x, y, enemy):
        best_coors = None
        best_val = -1
        for coors in array_area(x, y):
            try:
                if coors['x'] >= 0 and coors['y'] >= 0 and not (enemy.y == coors['y'] and enemy.x == coors['x']):
                    value = area.get_value(coors['x'], coors['y'])
                    if value == '.':
                        continue
                    # todo: enemy not here
                    elif best_val < int(value) and int(value) < MAX_HEIGHT:
                        best_val, best_coors = int(value), coors.copy()
                        # print("value {0}".format(value), file=sys.stderr)
            except Exception as e:
                continue
        return best_coors, best_val

area = Area()
units_per_player = int(input())
player = Player()
enemy = Player()
# game loop
while True:
    area.b_map()
    player.scan_pos()
    enemy.scan_pos()
    player.get_legal_actions()
    player.run(area, enemy)
    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)

