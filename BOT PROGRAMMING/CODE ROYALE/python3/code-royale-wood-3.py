import sys
import math
import random


class OwnerType:
    NO_STRUCTURE = -1
    FRIENDLY = 0
    ENEMY = 1


def dist(x1, y1, x2, y2):
    return math.hypot(x2 - x1, y2 - y1)


class StructureType:
    NO_STRUCTURE = -1
    MINE = 0
    TOWER = 1
    BARRACS = 2


class Site:
    def __init__(self, site_id, x, y, radius):
        self.site_id, self.x, self.y, self.radius = site_id, x, y, radius
        self.gold = 0
        self.max_gold = 0
        self.structure_type = StructureType.NO_STRUCTURE
        self.owner = OwnerType.NO_STRUCTURE
        self.param_1 = 0
        self.param_2 = 0

    def set_data(self, gold, max_gold, structure_type, owner, param_1, param_2):
        self.gold, self.max_gold, self.structure_type, self.owner, self.param_1, self.param_2 = gold, max_gold, structure_type, owner, param_1, param_2

    def __repr__(self):
        return '<Site> x:{} y:{}'.format(self.x, self.y)


class UnitType:
    QUEEN = -1
    KNIGHT = 0
    ARCHER = 1
    GIANT = 2
    COSTS = {0: 80, 1: 100, 2: 140}


class Unit:
    def __init__(self, x, y, owner, unit_type, health):
        self.x, self.y, self.owner, self.unit_type, self.health = x, y, owner, unit_type, health


class Queen:
    RADIUS = 30
    SPEED = 60

    def __init__(self):
        self.set_data(0, 0, 0, 0, 0)

    def set_data(self, x, y, owner, unit_type, health):
        self.x, self.y, self.owner, self.unit_type, self.health = x, y, owner, unit_type, health


class ValidActions:
    WAIT = 'WAIT'
    MOVE = 'MOVE {} {}'
    BUILD = 'BUILD {} {}'


class Action:
    def __init__(self, action=ValidActions.WAIT, params=[]):
        self.set_data(action, params)

    def set_data(self, action=ValidActions.WAIT, params=[]):
        self.action = action
        self.params = params

    def __str__(self):
        print(self.action, self.params, file=sys.stderr)
        return self.action.format(*self.params)


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
class Game:
    WIDTH = 1920
    HEIGHT = 1000
    MAX_HP = 800
    we_need_types = [
        # {'type': 'MINE', 'count': 2, 'structure_type': StructureType.MINE},
        {'type': 'BARRACKS-KNIGHT', 'count': 1, 'structure_type': StructureType.BARRACS},
        {'type': 'TOWER', 'count': 3, 'structure_type': StructureType.TOWER},
    ]
    we_need_units = [
        {'type': UnitType.KNIGHT, 'priority': 3},
        {'type': UnitType.ARCHER, 'priority': 1},
        {'type': UnitType.GIANT, 'priority': 2}
    ]
    corner = None

    def __init__(self):
        self._step = 0
        self._tower_to_improve = None
        self.corner = None
        self.train = []
        self.num_sites = int(input())
        self.gold = 0
        self.touched_site = 0
        self.sites = {}
        self._action = Action()
        for i in range(self.num_sites):
            site_id, x, y, radius = [int(j) for j in input().split()]
            self.sites[site_id] = Site(site_id, x, y, radius)
        self.my_queen = Queen()
        self.en_queen = Queen()
        self.num_units = 0
        self.units = []

    def _scan(self):
        self.gold, self.touched_site = [int(i) for i in input().split()]
        self._scan_sites()
        self._scan_units()
        self._step += 1

    def _scan_sites(self):
        # touched_site: -1 if none
        for i in range(self.num_sites):
            site_id, gold, max_gold, structure_type, owner, param_1, param_2 = [int(j) for j in input().split()]
            self.sites[site_id].set_data(gold, max_gold, structure_type, owner, param_1, param_2)

    def _scan_units(self):
        self.num_units = int(input())
        self.units.clear()
        for i in range(self.num_units):
            # unit_type: -1 = QUEEN, 0 = KNIGHT, 1 = ARCHER
            x, y, owner, unit_type, health = [int(j) for j in input().split()]
            self.units.append(Unit(x, y, owner, unit_type, health))
            if (UnitType.QUEEN == unit_type):
                if owner == OwnerType.FRIENDLY:
                    self.my_queen.set_data(x, y, owner, unit_type, health)
                    if (not (self.corner)):
                        self.corner = {
                            'x': [self.WIDTH, 0][x < self.WIDTH / 2],
                            'y': [self.HEIGHT, 0][y < self.HEIGHT / 2],
                        }
                else:
                    self.en_queen.set_data(x, y, owner, unit_type, health)

    def get_closest_site(self, sites, to):
        distance = self.HEIGHT * self.WIDTH
        build = None
        for site_id, site in sites.items():
            dis_site = dist(self.corner['x'], self.corner['x'], site.x, site.y)
            if (dis_site < distance):
                distance = dis_site
                build = site
        return build

    def get_farest_to_queen(self, sites):
        distance = 0
        build = None
        for site_id, site in sites.items():
            dis_site = dist(self.my_queen.x, self.my_queen.y, site.x, site.y)
            if (dis_site > distance):
                distance = dis_site
                build = site
        return build

    def get_closest_to_queen(self, sites):
        distance = self.HEIGHT * self.WIDTH
        build = None
        for site_id, site in sites.items():
            dis_site = dist(self.my_queen.x, self.my_queen.y, site.x, site.y)
            if (dis_site < distance):
                distance = dis_site
                build = site
        return build

    def filter_sites_by_owner(self, sites, owner):
        return {k: v for k, v in sites.items() if v.owner == owner}

    def filter_sites_by_type(self, sites, structure_type):
        return {k: v for k, v in sites.items() if v.structure_type == structure_type}

    def filter_sites_by_build_type(self, sites, build_type):
        return {k: v for k, v in sites.items() if v.param_2 == build_type}

    def filter_sites_by_ready(self, sites):
        return {k: v for k, v in sites.items() if v.param_1 == 0}

    def filter_sites_by_uncomplited_mines(self, sites):
        return {k: v for k, v in sites.items() if v.param_1 < v.max_gold}

    def filter_sites_by_complited_mines(self, sites):
        return {k: v for k, v in sites.items() if v.param_1 >= v.max_gold}

    def filter_by_distance(self, sites, coors):
        return {k: v for k, v in sites.items() if
                dist(coors['x'], coors['y'], v.x, v.y) < (self.WIDTH + self.HEIGHT) / 3}

    def _get_ready_to_build(self):
        sites = self.filter_by_distance(self.sites, self.corner)
        sites = self.filter_sites_by_owner(sites, OwnerType.NO_STRUCTURE)
        sites = self.filter_sites_by_type(sites, StructureType.NO_STRUCTURE)
        return sites

    def _get_uncomplited_mines(self):
        sites = self.filter_by_distance(self.sites, self.corner)
        sites = self.filter_sites_by_type(sites, StructureType.MINE)
        sites = self.filter_sites_by_uncomplited_mines(sites)
        print(sites, file=sys.stderr)
        return sites

    def _get_best_mine(self):
        sites = self._get_uncomplited_mines()
        if (len(sites) == 0):
            sites = self._get_ready_to_build()
            sites = {k: v for k, v in sites.items() if v.gold != 0 and v.max_gold != 0}
            # todo and v.gold==0 and v.max_gold==0
        print(sites, file=sys.stderr)
        return self.get_closest_site(sites, self.my_queen)

    def _get_best_barracs(self):
        sites = self._get_ready_to_build()
        return self.get_closest_site(sites, self.my_queen)

    def _get_best_tower(self):
        if (self._tower_to_improve and self._tower_to_improve.param_1 < 790):
            return self._tower_to_improve
        self._tower_to_improve = None
        sites = self._get_ready_to_build()
        return self.get_closest_site(sites, self.my_queen)

    def _what_to_build(self):
        build, build_type = None, None
        my_sites = self.filter_sites_by_owner(self.sites, OwnerType.FRIENDLY)
        for we_need in self.we_need_types:
            sites = self.filter_sites_by_type(my_sites, we_need['structure_type'])
            if (StructureType.MINE == we_need['structure_type']):
                sites = self.filter_sites_by_complited_mines(sites)
            if (len(sites) >= we_need['count']):
                continue
            if (we_need['structure_type'] == StructureType.MINE):
                build = self._get_best_mine()
            elif (we_need['structure_type'] == StructureType.BARRACS):
                build = self._get_best_barracs()
            elif (we_need['structure_type'] == StructureType.TOWER):
                build = self._get_best_tower()
                if (build):
                    self._tower_to_improve = build
            if build:
                build_type = we_need['type']
                break
        return [build, build_type]

    def _get_tower_to_improve(self):
        if (self._tower_to_improve and self._tower_to_improve.param_1 < 790):
            return self._tower_to_improve
        sites = self.filter_sites_by_owner(self.sites, OwnerType.FRIENDLY)
        sites = self.filter_sites_by_type(sites, StructureType.TOWER)
        best = None
        best_value = 0
        for site in sites.values():
            distance = dist(self.my_queen.x, self.my_queen.y, site.x, site.y)
            health = site.param_1
            if (1 / health > best_value):
                best_value = 1 / health
                best = site
        self._tower_to_improve = best
        return best

    def _under_creeps_attack(self):
        return [v for v in self.units if
                v.owner == OwnerType.ENEMY and dist(self.my_queen.x, self.my_queen.y, v.x, v.y) < 200]

    def _get_result(self):
        creeps = self._under_creeps_attack()
        if (len(creeps) > 0):
            if (self._tower_to_improve and self._tower_to_improve.param_1 < 790):
                self._action.set_data(ValidActions.BUILD, [self._tower_to_improve.site_id, 'TOWER'])
                return True
            empty_towers = self._get_ready_to_build()
            empty_tower = self.get_farest_to_queen(empty_towers)
            if (empty_tower):
                self._tower_to_improve = empty_tower
                self._action.set_data(ValidActions.BUILD, [empty_tower.site_id, 'TOWER'])
                return True

            sites = self.filter_sites_by_owner(self.sites, OwnerType.FRIENDLY)
            sites = self.filter_sites_by_type(sites, StructureType.TOWER)
            best_tower = self.get_farest_to_queen(empty_towers)
            if (best_tower):
                self._tower_to_improve = best_tower
                self._action.set_data(ValidActions.BUILD, [best_tower.site_id, 'TOWER'])
                return True

        build, build_type = self._what_to_build()
        if (build and build_type):
            self._action.set_data(ValidActions.BUILD, [build.site_id, build_type])
        else:
            tower_to_improve = self._get_tower_to_improve()
            if (tower_to_improve):
                self._action.set_data(ValidActions.BUILD, [tower_to_improve.site_id, 'TOWER'])
            elif (self.corner):
                self._action.set_data(ValidActions.MOVE, [self.corner['x'], self.corner['y']])
            else:
                self._action.set_data(ValidActions.WAIT, [])

    def _get_train_string(self):
        can_train_ids = []
        sites = self.filter_sites_by_owner(self.sites, OwnerType.FRIENDLY)
        sites = self.filter_sites_by_type(sites, StructureType.BARRACS)
        sites = self.filter_sites_by_ready(sites)
        can_train_ids = sites.keys()
        # random.shuffle(can_train_ids)
        app_string, can_spend = '', 0
        for train_id in can_train_ids:
            if (UnitType.COSTS[self.sites[train_id].param_2] < self.gold):
                can_spend += 80
                app_string += ' {}'.format(train_id)
                break
        return "TRAIN{}".format(app_string)

    def run(self):
        while True:
            self._scan()
            self._get_result()
            # Write an action using print
            # To debug: print("Debug messages...", file=sys.stderr)
            print(self._action)
            print(self._get_train_string())


game = Game()
game.run()