import sys
import math

MAX_HEIGHT = 4


class Area:
    DIRECTIONS = {
        'N': {'x': 0, 'y': -1},
        'NE': {'x': 1, 'y': -1},
        'E': {'x': 1, 'y': 0},
        'SE': {'x': 1, 'y': 1},
        'S': {'x': 0, 'y': 1},
        'SW': {'x': -1, 'y': 1},
        'W': {'x': -1, 'y': 0},
        'NW': {'x': -1, 'y': -1}
    }
    size = None
    map = []

    def __init__(self):
        self.size = int(input())

    def build_map(self):
        self.map = []
        for i in range(self.size):
            self.map.append(list(input()))

    def get_value(self, x, y):
        return self.map[y][x]

    def obj(x, y, d):
        return {'x': x, 'y': y, 'd': d}

    def array_area(x, y):
        return [
            self.obj(x - 1, y, 'W'),
            self.obj(x - 1, y - 1, 'NW'),
            self.obj(x, y - 1, 'N'),
            self.obj(x + 1, y - 1, 'NE'),
            self.obj(x + 1, y, 'E'),
            self.obj(x + 1, y + 1, 'SE'),
            self.obj(x, y + 1, 'S'),
            self.obj(x - 1, y + 1, 'SW')
        ]

    def get_corrs_from_direction(self, x, y, d):
        return {'x': x + self.DIRECTIONS[d]['x'], 'y': y + self.DIRECTIONS[d]['y']}

class Player():
    x = y = 0
    _title = ''

    def __init__(self, title):
        self.title = title

    def scan_pos(self):
        self.x, self.y = [int(j) for j in input().split()]

class Enemy(Player):
    pass

class Friend(Player):
    def get_legal_actions(self):
        legal_actions = int(input())
        for i in range(legal_actions):
            atype, index, dir_1, dir_2 = input().split()
            index = int(index)

    def run(self, area, enemy):
        current_height = int(area.get_value(self.x, self.y))
        print("current_height {0}".format(current_height), file=sys.stderr)
        move_to, new_height = self.get_best_coors_to_move(area, current_height, self.x, self.y, enemy)
        build_to, new_height2 = self.get_best_coors_to_build(area, new_height, move_to['x'], move_to['y'], enemy)
        print("move_to {0} build_to {1}".format(move_to, build_to), file=sys.stderr)
        # move_to = self.get_best_coors_to_build(area, current_height)
        print("MOVE&BUILD 0 {0} {1}".format(move_to['d'], build_to['d']))

class Action():
    area = None
    units_per_player = 0
    players = []
    enemies = []
    legal_actions = []
    legal_actions_list = []
    our_points = []
    enemy_points = []

    def __init__(self):
        self.area = Area()
        self.units_per_player = int(input())
        self._init_players()
        self._init_enemies()

    def _init_players(self):
        for i in range(self.units_per_player):
            self.players.append(Friend('Player ' + str(i)))
            # print("Players Init {0}".format(self.players), file=sys.stderr)

    def _init_enemies(self):
        for i in range(self.units_per_player):
            self.enemies.append(Enemy('Enemy ' + str(i)))
            # print("Enemies Init {0}".format(self.enemies), file=sys.stderr)

    def run(self):
        while True:
            self.area.build_map()
            for i in range(self.units_per_player):
                self.players[i].scan_pos()
            for i in range(self.units_per_player):
                self.enemies[i].scan_pos()
            self.legal_actions = int(input())
            self.legal_actions_list.clear()
            for i in range(self.legal_actions):
                atype, index, dir_1, dir_2 = input().split()
                index = int(index)
                self.legal_actions_list.append({'atype': atype, 'index': index, 'dir_1': dir_1, 'dir_2': dir_2})
            self.player_actions()

    def player_actions(self):
        action = self.unique_situation_check()
        if action is None:
            action = self.get_best_variant_to_move()
        if (action == None):
            print("MOVE&BUILD 0 N S")
            print("MOVE&BUILD 1 N S")
        else:
            print("{0} {1} {2} {3}".format(action['atype'], action['index'], action['dir_1'], action['dir_2']))

    def unique_situation_check(self):
        # проверить удачные комбинации. Возможность столкнуть врага, захватить точку(пустую или врага, защитить свою точку)
        pass

    def get_best_variant_to_move(self):
        best_action = None
        best_val = -1
        for action in self.legal_actions_list:
            cur_p = self.players[action['index']]
            cur_h = int(self.area.get_value(cur_p.x, cur_p.y))
            try:
                if (action['atype'] == 'PUSH&BUILD'):
                    pass
                    # if is_enemy_oncoors():
                    # check is enemy here
                else:
                    move_coors = self.area.get_corrs_from_direction(cur_p.x, cur_p.y, action['dir_1'])
                    move_height = self.area.get_value(move_coors['x'], move_coors['y'])
                    if move_height == '.':
                        continue
                    build_coors = self.area.get_corrs_from_direction(move_coors['x'], move_coors['y'],
                                                                     action['dir_2'])
                    build_height = self.area.get_value(build_coors['x'], build_coors['y'])
                    if build_height == '.':
                        continue
                    if (self.check_move_height(best_val, move_height, cur_h) and self.check_build_height(
                            build_height)):
                        best_val = int(move_height)
                        best_action = action

            except IndexError:
                continue
            return best_action

    def check_move_height(self, best_val, move_height, cur_h):
        return best_val <= int(move_height) and int(move_height) <= cur_h + 1 and int(move_height) < MAX_HEIGHT

    def check_build_height(self, build_height):
        return int(build_height) < MAX_HEIGHT

    def is_friend_on_pos(self):
        pass

    def is_enemy_on_pos(self):
        pass

    def builded4_point_is_your(self):
        pass

action = Action()
action.run()