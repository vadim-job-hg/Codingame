import sys
import math


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
def calc_distance(x, y, x2, y2):
    return math.sqrt(((x2 - x) ** 2) + ((y2 - y) ** 2))


class Path():
    x = None
    y = None
    trust = None

    def __init__(self, x, y, trust):
        self.x = x
        self.y = y
        self.trust = trust

    def getString(self):
        return "{0} {1} {2}".format(self.x, self.y, self.trust)


class Coordinates():
    pass


class Pod():
    x = None
    y = None
    next_checkpoint_x = None
    next_checkpoint_y = None
    next_checkpoint_angle = 0
    next_checkpoint_dist = 0
    opponent_x = None
    opponent_y = None
    path = None
    boost_not_used = True

    _path_points = []
    _current_speed = 0
    _all_path_points_known = False
    _current_taktik = "regular"

    # regular - simple tactick, shield - if we gonna crush, drift - drift untill speed 0, attack - lets attack enemy, round - vector calculation path
    def getData(self):
        x, y, nx, ny, nd, na = [int(i) for i in input().split()]
        ox, oy = [int(i) for i in input().split()]
        self.x = x
        self.y = y
        self.next_checkpoint_x = nx
        self.next_checkpoint_y = ny
        self.next_checkpoint_angle = na
        self.next_checkpoint_dist = nd
        self.opponent_x = ox
        self.opponent_y = oy

    def _calculateSpeed(self):
        pass

    def _getMoveVector(self):
        pass

    def _getNextCheckpoint(self):  # checkpoint after current
        pass

    def _calculatePathParams(self):
        self._calculateSpeed()
        if self.next_checkpoint_angle > 90 or self.next_checkpoint_angle < -90:
            thrust = 0
        else:
            thrust = 100

        if self.next_checkpoint_dist > 7000 and (-5 < self.next_checkpoint_angle < 5) and self.boost_not_used:
            self.boost_not_used = False
            thrust = "BOOST"

        if self.next_checkpoint_dist < 2500:
            thrust = 50

        if self.next_checkpoint_dist < 1000:
            thrust = 100

        return Path(self.next_checkpoint_x, self.next_checkpoint_y, thrust)

    def calculatePath(self):
        self.path = self._calculatePathParams()

    def run(self):
        if self.path is not None:
            print(self.path.getString())
        else:
            raise Exception('OOOPS!')


avaliable_boost = True
pod = Pod()
while True:
    pod.getData()
    pod.calculatePath()
    pod.run()
