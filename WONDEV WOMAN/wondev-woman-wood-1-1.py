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
    pass


class Action():
    area = None
    units_per_player = 0
    players = []
    enemies = []
    legal_actions = []
    legal_actions_list = {}
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

    def _get_legal_actions_list(self):
        self.legal_actions = int(input())
        self.legal_actions_list.clear()
        for i in range(self.legal_actions):
            atype, index, dir_1, dir_2 = input().split()
            self.legal_actions_list.setdefault(int(index), {}).setdefault(dir_1, []).append(
                {'dir_2': dir_2, 'atype': atype})
        print("Legal Actions {0}".format(self.legal_actions_list), file=sys.stderr)

        def run(self):
            while True:
                self.area.build_map()
                for i in range(self.units_per_player):
                    self.players[i].scan_pos()
                for i in range(self.units_per_player):
                    self.enemies[i].scan_pos()
                self._get_legal_actions_list()
                self.player_actions()

        def player_actions(self):
            action = self.unique_situation_check()
            if action is None:
                action = self.get_best_variant_to_move()
            if action is not None:
                print("{0} {1} {2} {3}".format(action['atype'], action['index'], action['dir_1'], action['dir_2']))

        def unique_situation_check(self):
            # проверить удачные комбинации. Возможность столкнуть врага, захватить точку(пустую или врага, защитить свою точку)


            pass

        def get_best_variant_to_move(self):
            for index, player_actions in self.legal_actions_list.items():

                for act_direction, action_data in player_actions.items():

                    for data in action_data:
                        pass

            return None
            best_action = None
            best_val = best_val2 = -1
            # print(self.legal_actions_list, file=sys.stderr)
            for action in self.legal_actions_list:
                cur_p = self.players[action['index']]
                cur_h = int(self.area.get_value(cur_p.x, cur_p.y))
                try:
                    if (action['atype'] == 'PUSH&BUILD'):
                        print(action, file=sys.stderr)
                        push_coors = self.area.get_corrs_from_direction(cur_p.x, cur_p.y, action['dir_1'])
                        push_height = self.area.get_value(move_coors['x'], move_coors['y'])
                        if push_height == '.':
                            continue
                        push_dir = self.area.get_corrs_from_direction(push_coors['x'], push_coors['y'],
                                                                      action['dir_2'])
                        push_dir_height = self.area.get_value(push_coors['x'], push_coors['y'])

                        if push_dir_height == '.':
                            continue

                        if ((1 <= cur_h <= 3) and 2 < int(push_height) < MAX_HEIGHT and int(push_dir_height) < 2
                            and self.check_build_height(push_dir_height)
                            and not (self.is_friend_on_pos(push_dir['x'], push_dir['y'], action['index']))
                            and self.is_enemy_on_pos(push_coors['x'], push_coors['y'])
                            and not (self.is_enemy_on_pos(push_dir['x'], push_dir['y']))
                            ):
                            best_val = int(push_height)
                            best_val2 = int(push_dir_height)
                            best_action = action
                            break
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
                        if (self.check_move_height(best_val, best_val2, move_height, build_height,
                                                   cur_h) and self.check_build_height(
                                build_height)  # and int(build_height)>=best_val2
                            and not (self.is_friend_on_pos(move_coors['x'], move_coors['y'], action['index']))
                            and not (self.is_friend_on_pos(build_coors['x'], build_coors['y'], action['index']))
                            and not (self.is_enemy_on_pos(move_coors['x'], move_coors['y']))
                            and not (self.is_enemy_on_pos(build_coors['x'], build_coors['y']))
                            ):
                            best_val = int(move_height)
                            best_val2 = int(build_height)
                            best_action = action

                except IndexError:
                    continue
            return best_action

        def check_move_height(self, best_val, best_val2, move_height, build_height, cur_h):
            return (best_val < int(move_height) or (
            (int(build_height) <= int(move_height) + 1 or int(build_height) + 1 == int(cur_h)) and best_val == int(
                move_height)) and best_val2 < int(build_height)) and int(move_height) <= cur_h + 1 and int(
                move_height) < MAX_HEIGHT

        def check_build_height(self, build_height):
            return int(build_height) < MAX_HEIGHT

        def is_friend_on_pos(self, x, y, ind):
            for i in range(self.units_per_player):
                if x == self.players[i].x and y == self.players[i].y and i != ind:
                    return True
            return False

        def is_enemy_on_pos(self, x, y):
            for i in range(self.units_per_player):
                if x == self.enemies[i].x and y == self.enemies[i].y:
                    return True
            return False

        def builded4_point_is_your(self):
            pass

    action = Action()
    action.run()