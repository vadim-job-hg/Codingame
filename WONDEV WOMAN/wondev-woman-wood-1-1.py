import sys
import math

MAX_HEIGHT = 4
MAX_SIZE = 7


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

    def array_area(self, x, y):
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
    our_points =  set()
    enemy_points = set()

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
            self.legal_actions_list.setdefault(int(index), {}).setdefault(atype, {}).setdefault(dir_1, []).append(dir_2)
            # print("Legal Actions {0}".format(self.legal_actions_list), file=sys.stderr)

    def run(self):
        while True:
            self.area.build_map()
            for i in range(self.units_per_player):
                self.players[i].scan_pos()
            for i in range(self.units_per_player):
                self.enemies[i].scan_pos()
            self._get_catched_points()
            self._get_legal_actions_list()
            self.player_actions()

    def player_actions(self):
        action = self.unique_situation_check()
        if action is None:
            action = self.get_best_variant_to_act()
        if action is not None:
            print("{0} {1} {2} {3}".format(action['atype'], action['index'], action['dir_1'], action['dir_2']))

    def _get_catched_points(self):
        for i in range(self.units_per_player):
            height = int(self.area.get_value(self.players[i].x, self.players[i].y))
            if height == 3:
                self.our_points.add(self.xynum(self.players[i].x, self.players[i].y))
                self.enemy_points.discard(self.xynum(self.players[i].x, self.players[i].y))
        for i in range(self.units_per_player):
            height = int(self.area.get_value(self.enemies[i].x, self.enemies[i].y))
            if height == 3:
                self.enemy_points.add(self.xynum(self.players[i].x, self.players[i].y))
                self.our_points.discard(self.xynum(self.players[i].x, self.players[i].y))

    def xynum(self, x, y):
        return x + y * 10  # (MAX_SIZE+1)

    def unique_situation_check(self):
        # проверить удачные комбинации. Возможность столкнуть врага, захватить точку(пустую или врага, защитить свою точку)

        pass

    def get_best_variant_to_act(self):
        best_action = {}
        best_action_data = {
            'score': -1
        }
        for index, player_actions in self.legal_actions_list.items():
            print("index {0}".format(index), file=sys.stderr)
            current_player = self.players[index]
            current_height = int(self.area.get_value(current_player.x, current_player.y))
            for action, action_data in player_actions.items():
                try:
                    print("Action {0}".format(action), file=sys.stderr)
                    if action == 'PUSH&BUILD':
                        for dir_1, dir_data in action_data.items():
                            act_coors = self.area.get_corrs_from_direction(current_player.x, current_player.y, dir_1)
                            act_height = self.area.get_value(act_coors['x'], act_coors['y'])
                            is_enemy_on_pos = self.is_enemy_on_pos(act_coors['x'], act_coors['y'])
                            if act_height == '.' or not (is_enemy_on_pos):
                                continue
                            else:
                                act_height = int(act_height)
                                #print("act_height {0}".format(act_height), file=sys.stderr)
                                for dir_2 in dir_data:
                                    act2_coors = self.area.get_corrs_from_direction(act_coors['x'], act_coors['y'],
                                                                                    dir_2)
                                    act2_height = self.area.get_value(act2_coors['x'], act2_coors['y'])
                                    is_enemy_on_pos2 = self.is_enemy_on_pos(act2_coors['x'], act2_coors['y'])
                                    is_friend_on_pos2 = self.is_enemy_on_pos(act2_coors['x'], act2_coors['y'])
                                    if act2_height == '.' or is_enemy_on_pos2 or is_friend_on_pos2:
                                        continue
                                    else:
                                        act2_height = int(act2_height)
                                        score = (act2_height - act_height) + 1
                                        if act2_height < act_height < MAX_HEIGHT - 1 and score > best_action_data[
                                            'score']:
                                            best_action_data['score'] = score
                                            best_action['atype'], best_action['index'], best_action['dir_1'], \
                                            best_action['dir_2'] = action, index, dir_1, dir_2
                                        if act2_height < act_height and act_height == 2 and 10 > best_action_data[
                                            'score']:
                                            best_action_data['score'] = 10
                                            best_action['atype'], best_action['index'], best_action['dir_1'], \
                                            best_action['dir_2'] = action, index, dir_1, dir_2

                    elif action == 'MOVE&BUILD':
                        for dir_1, dir_data in action_data.items():
                            #print("dir_1 {0}".format(dir_1), file=sys.stderr)
                            act_coors = self.area.get_corrs_from_direction(current_player.x, current_player.y, dir_1)
                            act_height = self.area.get_value(act_coors['x'], act_coors['y'])
                            is_enemy_on_pos = self.is_enemy_on_pos(act_coors['x'], act_coors['y'])
                            is_friend_on_pos = self.is_friend_on_pos(act_coors['x'], act_coors['y'])
                            if act_height == '.' or is_enemy_on_pos or is_friend_on_pos:
                                continue
                            else:
                                act_height = int(act_height)
                                is_check_point = self.is_check_point(act_coors['x'], act_coors['y'])
                                if is_check_point and not (self.is_friends_check_point(act_coors['x'], act_coors['y'])):
                                    score_plus = 15
                                else:
                                    score_plus = 0
                                score = score_plus + act_height
                                if MAX_HEIGHT > act_height and best_action_data[
                                    'score'] < score and act_height <= current_height + 1:
                                    best_action_data['score'] = score
                                else:
                                    continue
                                best_score2 = -1
                                for dir_2 in dir_data:
                                    print("dir_2 {0}".format(dir_1), file=sys.stderr)
                                    act2_coors = self.area.get_corrs_from_direction(act_coors['x'], act_coors['y'],
                                                                                    dir_2)
                                    act2_height = self.area.get_value(act2_coors['x'], act2_coors['y'])
                                    is_enemy_on_pos2 = self.is_enemy_on_pos(act2_coors['x'], act2_coors['y'])
                                    is_friend_on_pos2 = self.is_friend_on_pos(act2_coors['x'], act2_coors['y'], index)
                                    if act2_height == '.' or is_enemy_on_pos2 or is_friend_on_pos2:
                                        continue
                                    else:
                                        act2_height = int(act2_height)
                                        score = act2_height
                                        if act2_height < MAX_HEIGHT and score > best_score2:
                                            best_score2 = score
                                            best_action['atype'], best_action['index'], best_action['dir_1'], \
                                            best_action['dir_2'] = action, index, dir_1, dir_2

                except IndexError:
                    continue
        print("Legal Actions {0}".format(best_action), file=sys.stderr)
        return best_action

    def is_check_point(self, x, y):
        return self.area.get_value(x, y) == '3'

    def is_enemy_check_point(self, x, y):
        pass

    def is_friends_check_point(self, x, y):
        return self.xynum(x, y) in self.our_points

    def is_friend_on_pos(self, x, y, ind=-1):
        for i in range(self.units_per_player):
            if x == self.players[i].x and y == self.players[i].y and i != ind:
                return True
        return False

    def is_enemy_on_pos(self, x, y):
        for i in range(self.units_per_player):
            if x == self.enemies[i].x and y == self.enemies[i].y:
                return True
        return False


action = Action()
action.run()