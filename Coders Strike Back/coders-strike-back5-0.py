import sys
import math


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

    def __init__(self, x, y, z):
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


def calc_distance(x, y, x2, y2):
    return math.sqrt(((x2 - x) ** 2) + ((y2 - y) ** 2))


class Path():
    x = None
    y = None
    trust = None

    def setPath(self, x, y, trust):
        self.x, self.y, self.trust = x, y, trust

    def getString(self):
        return "{0} {1} {2}".format(self.x, self.y, self.trust)


class PathPoint():
    x = None
    y = None

    def __init__(self, x, y):
        self.x, self.y = x, y

    def isEqual(self, x, y):
        return self.x == x and self.y == y


class Player():
    _title = ''
    x = 1000
    y = 1000
    speed = 0
    _direction = {"from": {"x": 0, "y": 0}, "to": {"x": 0, "y": 0}}

    def __init__(self, title):
        self._title = title

    def setParams(self, x, y):
        self.set_direction(self.x, self.y, x, y)
        self.speed, self.x, self.y = calc_distance(x, y, self.x, self.y), x, y
        print(self._title + ' speed: ' + str(self.speed), file=sys.stderr)

        def set_direction(self, x1, y1, x2, y2):
            self._direction = {"from": {"x": x1, "y": y1}, "to": {"x": x2, "y": y2}}

    class Pod():
        player = Player('player')
        opponent = Player('oponent')
        path = Path()

        next_checkpoint_x = None
        next_checkpoint_y = None
        next_checkpoint_angle = 0
        next_checkpoint_dist = 0
        boost_not_used = True
        all_path_points_known = False
        _lap = 1
        _path_points = []
        _pased = -1
        _current_taktik = "regular"

        # regular - simple tactick, shield - if we gonna crush, drift - drift untill speed 0, attack - lets attack enemy, round - vector calculation path
        def getData(self):
            x, y, nx, ny, nd, na = [int(i) for i in input().split()]
            ox, oy = [int(i) for i in input().split()]
            self.player.setParams(x, y)
            self.opponent.setParams(ox, oy)
            if not (self.next_checkpoint_x == nx and self.next_checkpoint_y == ny):
                if not (self.all_path_points_known):
                    self.addPathPoint(nx, ny)
                self.next_checkpoint_x, self.next_checkpoint_y = nx, ny
                self._pased = self._pased + 1
            self.next_checkpoint_angle = abs(na)
            self.next_checkpoint_dist = nd

        def addPathPoint(self, x, y):
            if (len(self._path_points) > 0 and self._path_points[0].isEqual(x, y)):
                self.all_path_points_known = True
            else:
                self._path_points.append(PathPoint(x, y))

        def _getTactick(self):
            # todo check shield
            if self.all_path_points_known:
                # todo: check if drift posible
                self._current_taktik = "regular"
            else:
                self._current_taktik = "regular"

        def _regularPath(self):  # todo: vector calculation
            if (self.next_checkpoint_angle > 90):
                self.path.setPath(self.next_checkpoint_x, self.next_checkpoint_y, 0)
            # todo: or last
            elif (self.next_checkpoint_dist > 6000 and self.next_checkpoint_angle < 5 and self.boost_not_used):
                self.boost_not_used = False
                self.path.setPath(self.next_checkpoint_x, self.next_checkpoint_y, "BOOST")
            else:
                self.path.setPath(self.next_checkpoint_x, self.next_checkpoint_y, 100)
                # Vectors Logik starts from here

        def _driftPath(self):
            pass

        def calculatePath(self):
            self._getTactick()
            getattr(self, "_" + self._current_taktik + "Path", "_regularPath")()

        def run(self):
            if self.path is not None:
                print(self.path.getString())
            else:
                raise Exception('OOOPS!')

    pod = Pod()
    while True:
        pod.getData()
        pod.calculatePath()
        pod.run()
