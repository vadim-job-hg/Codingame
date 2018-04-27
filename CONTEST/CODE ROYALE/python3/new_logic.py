import sys
import math
import random


class Point(object):
    """ Point class: Reprepsents a point in the x, y, z space. """

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return '{0}({1}, {2}, {3})'.format(self.__class__.__name__, self.x,
                                           self.y, self.z)

    def substract(self, point):
        """ Return a Point instance as the displacement of two points. """
        return Point(point.x - self.x, point.y - self.y, point.z - self.z)

    @classmethod
    def from_list(cls, l):
        """ Return a Point instance from a given list """

        x, y, z = map(float, l)
        return cls(x, y, z)


class Vector(Point):
    """ Vector class: Represents a vector in the x, y, z space. """

    def __init__(self, x, y, z=0):
        self.vector = [x, y, z]
        super(Vector, self).__init__(x, y, z)

    def add(self, number):
        """ Return a Vector instance as the product of the vector and a real
            number. """

        return self.from_list([x + number for x in self.vector])

    def multiply(self, number):
        """ Return a Vector instance as the product of the vector and a real
            number. """

        return self.from_list([x * number for x in self.vector])

    def magnitude(self):
        """ Return magnitude of the vector. """

        return (math.sqrt(reduce(lambda x, y: x + y,
                                 [x ** 2 for x in self.vector])))

    def sum(self, vector):
        """ Return a Vector instance as the vector sum of two vectors. """

        return (self.from_list([x + vector.vector[self.vector.index(x)]
                                for x in self.vector]))

    def substract(self, vector):
        """ Return a Vector instance as the vector difference of two vectors.
        """

        return (self.from_list([vector.vector[self.vector.index(x)] - x for x in
                                self.vector]))

    def dot(self, vector, theta=None):
        """ Return the dot product of two vectors. If theta is given then the
        dot product is computed as v1*v1 = |v1||v2|cos(theta). Argument theta
        is measured in degrees. """

        if theta is not None:
            return (self.magnitude() * vector.magnitude() *
                    math.degrees(math.cos(theta)))
        return (reduce(lambda x, y: x + y,
                       [x * vector.vector[self.vector.index(x)]
                        for x in self.vector]))

    def cross(self, vector):
        """ Return a Vector instance as the cross product of two vectors """

        return Vector((self.y * vector.z - self.z * vector.y),
                      (self.z * vector.x - self.x * vector.z),
                      (self.x * vector.y - self.y * vector.x))

    def angle(self, vector):
        """ Return the angle between two vectors in degrees. """

        return (math.degrees(math.acos((self.dot(vector) / (self.magnitude() *
                                                            vector.magnitude())))))

    def parallel(self, vector):
        """ Return True if vectors are parallel to each other. """

        if self.cross(vector).magnitude() == 0:
            return True
        return False

    def perpendicular(self, vector):
        """ Return True if vectors are perpendicular to each other. """

        if self.dot(vector) == 0:
            return True
        return False

    def non_parallel(self, vector):
        """ Return True if vectors are non-parallel. Non-parallel vectors are
            vectors which are neither parallel nor perpendicular to each other.
        """

        if (self.is_parallel(vector) is not True and
                    self.is_perpendicular(vector) is not True):
            return True
        return False

    @classmethod
    def from_points(cls, point1, point2):
        """ Return a Vector instance from two given points. """

        if isinstance(point1, Point) and isinstance(point2, Point):
            displacement = point1.substract(point2)
            return cls(displacement.x, displacement.y, displacement.z)
        raise TypeError


def dist(x1, y1, x2, y2):
    return math.hypot(x2 - x1, y2 - y1)


class OwnerType:
    NO_STRUCTURE = -1
    FRIENDLY = 0
    ENEMY = 1


class StructureType:
    NO_STRUCTURE = -1
    MINE = 0
    TOWER = 1
    BARRACS = 2


class ValidActions:
    WAIT = 'WAIT'
    MOVE = 'MOVE {} {}'
    BUILD = 'BUILD {} {}'


class UnitType:
    QUEEN = -1
    KNIGHT = 0
    ARCHER = 1
    GIANT = 2
    COSTS = {0: 80, 1: 100, 2: 140}
    NUMBER = {0: 4, 1: 2, 2: 1}
    SPEED = None  # todo
    DAMAGE = None  # todo
    RANGE = None  # todo
    TRAINING = None  # todo
    RADIUS = {0: 20, 1: 25, 2: 40, -1: 60}


class Coors:
    def __init__(self, x, y, radius=0):
        self.x, self.y = int(x), int(y)
        self.radius = radius

    def set_coors(self, x, y):
        self.x, self.y = x, y

    def dist(self, other):
        return dist(self.x, self.y, other.x, other.y)


class Site(Coors):
    def __init__(self, site_id, x, y, radius):
        super(Site, self).__init__(x, y, radius)
        self.site_id = site_id
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

    def check_eq(self, **kwargs):
        if (('owner' in kwargs) and self.owner != kwargs['owner']):
            return False

        if (('structure_type' in kwargs) and self.structure_type != kwargs['structure_type']):
            return False

        if (('param_1' in kwargs) and self.param_1 != kwargs['param_1']):  # Ready to build units
            return False

        if (('param_2' in kwargs) and self.param_2 != kwargs['param_2']):  # build_type
            return False

        return True

    def check_lg(self, **kwargs):
        if (('param_2' in kwargs) and self.param_2 < kwargs['param_2']):  # build_type
            return False

        return True

    def check_sm(self, **kwargs):
        if (('param_2' in kwargs) and self.param_2 > kwargs['param_2']):  # build_type
            return False

        return True


class Unit(Coors):
    def __init__(self, x, y, owner, unit_type, health):
        super(Unit, self).__init__(x, y, UnitType.RADIUS[unit_type])
        self.owner, self.unit_type, self.health = owner, unit_type, health


class Queen(Coors):
    SPEED = 60

    def __init__(self):
        self.set_data(0, 0, 0, 0, 0)

    def set_data(self, x, y, owner, unit_type, health):
        self.x, self.y, self.owner, self.unit_type, self.health = x, y, owner, unit_type, health
        self.radius = UnitType.RADIUS[-1]


class Action:
    def __init__(self, action=ValidActions.WAIT, params=[]):
        self.set_data(action, params)

    def set_data(self, action=ValidActions.WAIT, params=[]):
        self.action = action
        self.params = params

    def __str__(self):
        return self.action.format(*self.params)


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
class Game:
    WIDTH = 1920
    HEIGHT = 1000
    MAX_HP = 800
    MOVE_SPEED = 60
    we_need_types = [
        {'type': 'BARRACKS-KNIGHT', 'count': 1, 'structure_type': StructureType.BARRACS},
        {'type': 'MINE', 'count': 3, 'structure_type': StructureType.MINE},
        {'type': 'TOWER', 'count': 2, 'structure_type': StructureType.TOWER},
        {'type': 'MINE', 'count': 3, 'structure_type': StructureType.MINE},
    ]
    we_need_units = [
        {'types': [UnitType.KNIGHT], 'priority': 3},
        {'types': [UnitType.ARCHER], 'priority': 1},
        {'types': [UnitType.GIANT], 'priority': 2}
    ]
    corner = None

    def __init__(self):
        self._action = Action()
        self.strategy = None
        self._tower_to_improve = None
        self._step = 0
        self.corner = None
        self.num_sites = int(input())
        self.gold = 0
        self.touched_site = 0
        self.sites = {}
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
                        self._found_corner()
                else:
                    self.en_queen.set_data(x, y, owner, unit_type, health)

    def _found_corner(self):
        self.corner = Coors([self.WIDTH, 0][self.my_queen.x < self.WIDTH / 2],
                            [self.HEIGHT, 0][self.my_queen.y < self.HEIGHT / 2])

    def get_closest_coor(self, coors, coor):
        distance = self.HEIGHT * self.WIDTH
        result = None
        if isinstance(coors, dict):
            coors_list = coors.values()
        else:
            coors_list = coors
        for c in coors_list:  # todo: use lambda
            dis_result = c.dist(coor)
            if (dis_result < distance):
                distance = dis_result
                result = c
        return result

    def get_farest_coor(self, coors, coor):
        distance = 0
        result = None
        if isinstance(coors, dict):
            coors_list = coors.values()
        else:
            coors_list = coors
        for c in coors_list:  # todo: use lambda
            dis_result = c.dist(coor)
            if (dis_result > distance):
                distance = dis_result
                result = c
        return result

    def filter_sites_eq(self, sites, **kwargs):
        return {k: v for k, v in sites.items() if v.check_eq(**kwargs)}

    def filter_sites_by_uncomplited_mines(self, sites):
        return {k: v for k, v in sites.items() if v.param_1 < v.max_gold}

    def filter_sites_by_complited_mines(self, sites):
        return {k: v for k, v in sites.items() if v.param_1 >= v.max_gold}

    def filter_by_my_side(self, sites):
        return {k: v for k, v in sites.items() if
                (self.corner.x == 0 and v.x < 1010) or (self.corner.x != 0 and v.x > 990)}

    def _get_ready_to_build(self):
        sites = self.filter_by_my_side(self.sites)
        sites = self.filter_sites_eq(sites, owner=OwnerType.NO_STRUCTURE, struture_type=StructureType.NO_STRUCTURE)
        return sites

    def _get_uncomplited_mines(self):
        sites = self.filter_by_my_side(self.sites)
        sites = self.filter_sites_eq(sites, structure_type=StructureType.MINE, owner=OwnerType.FRIENDLY)
        sites = self.filter_sites_by_uncomplited_mines(sites)

        print(sites, file=sys.stderr)
        return sites

    def _get_best_mine(self):
        sites = self._get_uncomplited_mines()
        if (len(sites) == 0):
            sites = sites = {k: v for k, v in sites.items() if
                             v.gold != 0 and v.max_gold >= 4 and v.structure_type != StructureType.MINE}

        if (len(sites) == 0):
            sites = self._get_ready_to_build()
            sites = {k: v for k, v in sites.items() if
                     v.gold != 0 and v.max_gold >= 1 and v.structure_type != StructureType.MINE}
            # todo and v.gold==0 and v.max_gold==0
        print(sites, file=sys.stderr)
        return self.get_closest_coor(sites, self.my_queen)

    def _get_best_barracs(self):
        sites = self._get_ready_to_build()
        return self.get_closest_coor(sites, self.my_queen)

    def _get_best_tower_def(self):
        if (self._tower_to_improve and self._tower_to_improve.param_1 < 800):
            return self._tower_to_improve
        sites = self._get_ready_to_build()
        sites = {k: v for k, v in sites.items() if v.dist(self.corner) > 800 and v.x > 500 and v.x < 1200}
        return self.get_closest_coor(sites, self.my_queen)

    def _get_best_tower(self):
        if (self._tower_to_improve and self._tower_to_improve.param_1 < 800):
            return self._tower_to_improve
        sites = self._get_ready_to_build()
        # sites = {k: v for k, v in sites.items() if v.dist(self.corner) > 800 and v.x>500 and v.x<1200}
        return self.get_closest_coor(sites, self.my_queen)

    def _what_to_build(self):
        build, build_type = None, None
        my_sites = self.filter_sites_eq(self.sites, owner=OwnerType.FRIENDLY)
        for we_need in self.we_need_types:
            sites = self.filter_sites_eq(my_sites, structure_type=we_need['structure_type'])
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
        if (self._tower_to_improve and self._tower_to_improve.param_1 < 500):
            return self._tower_to_improve
        sites = self.filter_sites_eq(self.sites, owner=OwnerType.FRIENDLY, tower=StructureType.TOWER)
        best = None
        best_value = 0
        for site in sites.values():
            distance = dist(self.my_queen.x, self.my_queen.y, site.x, site.y)
            health = site.param_1
            if (health > 0 and 1 / health > best_value):
                best_value = 1 / health
                best = site
        self._tower_to_improve = best
        return best

    def _under_creeps_attack(self):
        return [v for v in self.units if
                v.owner == OwnerType.ENEMY and dist(self.my_queen.x, self.my_queen.y, v.x, v.y) < 250]

    def _get_result(self):
        # if (self.move_to):
        #    print(self.move_to.dist(self.my_queen), self.MOVE_SPEED, self.move_to.radius, file=sys.stderr)
        #    if (self.move_to.dist(self.my_queen) > self.MOVE_SPEED + self.move_to.radius):
        #        self._action.set_data(ValidActions.MOVE, [self.move_to.x, self.move_to.y])
        #    else:
        #        self.move_to = None

        creeps = self._under_creeps_attack()
        if (len(creeps) > 0):
            closest_creep = self.get_closest_coor(creeps, self.my_queen)
            sites = {k: v for k, v in self.sites.items() if
                     v.structure_type != StructureType.TOWER and v.dist(self.my_queen) < v.dist(closest_creep)}
            closest_site = self.get_closest_coor(sites, self.my_queen)
            if (closest_site):
                if (closest_site.structure_type != StructureType.TOWER):
                    self._action.set_data(ValidActions.BUILD, [closest_site.site_id, 'TOWER'])
                else:
                    # creep_vector = Vector(closest_creep.x, closest_creep.y, 0).substract(Vector(closest_site.x, closest_site.y, 0))
                    from_creep = Vector(closest_creep.x, closest_creep.y, 0).substract(
                        Vector(self.my_queen.x, self.my_queen.y, 0))
                    escape_vector = Vector(closest_site.x, closest_site.y, 0).sum(from_creep.multiply(2))
                    self._action.set_data(ValidActions.MOVE, [int(escape_vector.x), int(escape_vector.y)])
                return True

        build, build_type = self._what_to_build()
        if (build and build_type):
            if (self.my_queen.dist(build) > self.MOVE_SPEED + build.radius):
                self.move_to = build
                self._action.set_data(ValidActions.MOVE, [self.move_to.x, self.move_to.y])
                return True
            self._action.set_data(ValidActions.BUILD, [build.site_id, build_type])
        else:
            tower_to_improve = self._get_tower_to_improve()
            if (tower_to_improve):
                self._action.set_data(ValidActions.BUILD, [tower_to_improve.site_id, 'TOWER'])
            elif (self.corner):
                self._action.set_data(ValidActions.MOVE, [self.corner.x, self.corner.y])
            else:
                self._action.set_data(ValidActions.WAIT, [])

    def _get_train_string(self):
        can_train_ids = []
        sites = self.filter_sites_eq(self.sites, owner=OwnerType.FRIENDLY, structure_type=StructureType.BARRACS,
                                     param_1=0)
        can_train_ids = sites.keys()
        # random.shuffle(can_train_ids)
        app_string, can_spend = '', 0
        for train_id in can_train_ids:
            if (UnitType.COSTS[self.sites[train_id].param_2] < self.gold):
                can_spend += 80
                app_string += ' {}'.format(train_id)
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