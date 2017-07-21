import sys
import math
#
import numpy as np
from inspect import currentframe


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
    vector = np.array([0, 0, 0])

    def __init__(self, title):
        self._title = title

    def setParams(self, x, y):
        self.speed, self.x, self.y = calc_distance(x, y, self.x, self.y), x, y
        print(self._title + ' speed: ' + str(self.speed), file=sys.stderr)


        # _vector = math.vector(0, 0)

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
                if self.all_path_points_known:
                    self._current_taktik = "drift"
                else:
                    self._current_taktik = "regular"

            def _regularPath(self):  # todo: vector calculation
                thrust = 100
                rad = math.radians(self.next_checkpoint_angle)
                if self.next_checkpoint_dist > 6000 and self.next_checkpoint_angle < 5 and self.boost_not_used:
                    self.boost_not_used = False
                    thrust = "BOOST"
                elif (self.next_checkpoint_angle < 90):
                    perfectForce = self.next_checkpoint_dist * math.cos(rad) * 0.15
                    if 1000 < self.next_checkpoint_dist < 2500:
                        if self.player.speed > 150:
                            thrust = 50
                        elif self.player.speed > 100:
                            thrust = 70
                        elif self.player.speed > 50:
                            thrust = 90
                        else:
                            thrust = 100
                    elif (perfectForce > 100):
                        thrust = 100
                    elif (perfectForce < 0):
                        thrust = 0
                    else:
                        thrust = int(perfectForce)
                else:
                    thrust = 0
                self.path.setPath(self.next_checkpoint_x, self.next_checkpoint_y, thrust)

            def _driftPath(self):
                if self.player.speed > 300 or (self.next_checkpoint_dist < 1000 and self.player.speed > 200):
                    if (self.next_checkpoint_dist) > 1000:
                        self._regularPath()
                    else:
                        pp_next = self._path_points[(self._pased + 1) % len(self._path_points)]
                        self.path.setPath(pp_next.x, pp_next.y, 1)
                else:
                    self._regularPath()

            def calculatePath(self):
                self._getTactick()
                # print("_"+self._current_taktik+"Path", file=sys.stderr)
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
