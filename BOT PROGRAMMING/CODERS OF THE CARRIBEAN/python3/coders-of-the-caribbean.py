# https://github.com/waniz/katas_hackerrank_codingame_codewars/blob/master/codingame/contests/coders_of_the_carribbean/carribean.py
# https://www.codingame.com/ide/puzzle/coders-of-the-caribbean
import sys
import time
import math


class Ship:
    def __init__(self, id_, type_, x_, y_, arg1, arg2, arg3, arg4):
        self.id = id_
        self.type = type_
        self.r = x_
        self.q = y_
        self.axial_x = None
        self.axial_y = None
        self.axial_z = None
        self.arg_1 = arg1
        self.arg_2 = arg2
        self.arg_3 = arg3
        self.arg_4 = arg4


class Barrel:
    def __init__(self, id_, type_, x_, y_, arg1):
        self.id = id_
        self.type = type_
        self.r = x_
        self.q = y_
        self.axial_x = None
        self.axial_y = None
        self.axial_z = None
        self.arg_1 = arg1


class GridHelper:

    @staticmethod
    def fill_axial(my_target):
        my_target.axial_x = my_target.q
        my_target.axial_z = my_target.r
        my_target.axial_y = - my_target.axial_x - my_target.axial_z


class Bot:
    def __init__(self, ships, barrels):
        self.ships = ships
        self.barrels = barrels

    @staticmethod
    def get_distance(a, b):
        distance = (abs(a.q - b.q) + abs(a.q + a.r - b.q - b.r) + abs(a.r - b.r)) / 2
        return distance

    def get_the_closest_barrel(self, ship_):
        the_min_dist = 10000
        barrel_best = None
        for barrel_ in self.barrels:
            dist = self.get_distance(ship_, barrel_)
            if dist < the_min_dist:
                the_min_dist = dist
                barrel_best = barrel_
        # print('DEBUG: best distance: ', the_min_dist, file=sys.stderr)
        return barrel_best

    def get_the_fire_target(self, ship_):
        ship_best = None
        for ship_iter in self.ships:
            if ship_iter.arg_4 == 1:
                continue
            dist = self.get_distance(ship_, ship_iter)
            if dist < 10:
                ship_best = ship_iter
                print('DEBUG: distance to enemy: %s target: %s %s' % (dist, ship_iter.r, ship_iter.q), file=sys.stderr)
                return ship_best
        return ship_best

while True:
    # initial code
    ships_arr, barrels_arr = [], []
    # end initial code

    my_ship_count = int(input())
    entity_count = int(input())
    for _ in range(entity_count):
        entity_id, entity_type, x, y, arg_1, arg_2, arg_3, arg_4 = input().split()
        if entity_type == 'SHIP':
            ships_arr.append(Ship(int(entity_id), entity_type, int(x), int(y),
                                  int(arg_1), int(arg_2), int(arg_3), int(arg_4)))
        if entity_type == 'BARREL':
            barrels_arr.append(Barrel(int(entity_id), entity_type, int(x), int(y), int(arg_1)))

    # logic starts here
    start_move_timer = time.time()

    # coordinate conversion to axial coordinates
    grid_converter = GridHelper()
    for ship in ships_arr:
        grid_converter.fill_axial(ship)
    for barrel in barrels_arr:
        grid_converter.fill_axial(barrel)

    for my_ship in ships_arr:
        if my_ship.arg_4 != 1:
            continue

        my_bot = Bot(ships_arr, barrels_arr)

        # simple get the closest barrel
        best_barrel = my_bot.get_the_closest_barrel(my_ship)
        fire_target = my_bot.get_the_fire_target(my_ship)

        if best_barrel:
            print('MOVE %s %s' % (best_barrel.r, best_barrel.q))
            if fire_target:
                print('FIRE %s %s' % (fire_target.r, fire_target.q))
        else:
            print('WAIT')
    print('Debug: move spent: ', round(time.time() - start_move_timer, 4), file=sys.stderr)