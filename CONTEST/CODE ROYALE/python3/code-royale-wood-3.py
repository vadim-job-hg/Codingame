import sys
import math


class OwnerType:
    NO_STRUCTURE = -1
    FRIENDLY = 0
    ENEMY = 1


def dist(x1, y1, x2, y2):
    return math.hypot(x2 - x1, y2 - y1)


class StructureType:
    NO_STRUCTURE = -1
    BARRACS = 2


class Site:
    def __init__(self, site_id, x, y, radius):
        self.site_id, self.x, self.y, self.radius = site_id, x, y, radius
        self.ignore_1 = 0
        self.ignore_2 = 0
        self.structure_type = StructureType.NO_STRUCTURE
        self.owner = OwnerType.NO_STRUCTURE
        self.param_1 = 0
        self.param_2 = 0

    def set_data(self, ignore_1, ignore_2, structure_type, owner, param_1, param_2):
        self.ignore_1, self.ignore_2, self.structure_type, self.owner, self.param_1, self.param_2 = ignore_1, ignore_2, structure_type, owner, param_1, param_2


class UnitType:
    QUEEN = -1
    KNIGHT = 0
    ARCHER = 1


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
    BUILD = 'BUILD {} BARRACKS-{}'


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

    def __init__(self):
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

    def _scan_sites(self):
        # touched_site: -1 if none
        for i in range(self.num_sites):
            # ignore_1: used in future leagues
            # ignore_2: used in future leagues
            # structure_type: -1 = No structure, 2 = Barracks
            # owner: -1 = No structure, 0 = Friendly, 1 = Enemy
            site_id, ignore_1, ignore_2, structure_type, owner, param_1, param_2 = [int(j) for j in input().split()]
            self.sites[site_id].set_data(ignore_1, ignore_2, structure_type, owner, param_1, param_2)

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

    def _get_closest_netral_site(self):
        distance = self.HEIGHT * self.WIDTH
        build = None
        for site_id, site in self.sites.items():
            if OwnerType.NO_STRUCTURE == site.owner:
                dis_site = dist(self.my_queen.x, self.my_queen.y, site.x, site.y)
                if (dis_site < distance):
                    distance = dis_site
                    build = site
        return build

    def _get_result(self):
        build = self._get_closest_netral_site()
        if (build):
            self._action.set_data(ValidActions.BUILD, [build.site_id, 'KNIGHT'])
        else:
            self._action.set_data(ValidActions.WAIT)

    def _get_train_string(self):
        can_train_id = []
        for site_id, site in self.sites.items():
            if OwnerType.FRIENDLY == site.owner and StructureType.BARRACS == site.structure_type:
                can_train_id.append(str(site_id))

        app_string = ''
        if (len(can_train_id) > 0 and self.gold > 80):
            app_string = ' ' + can_train_id[0]

        return "TRAIN" + app_string

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