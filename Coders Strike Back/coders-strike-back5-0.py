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
    _x = None
    _y = None

    def __init__(self, x, y):
        self._x, self.y = x, y


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

            _path_points = []
            _all_path_points_known = False
            _current_taktik = "regular"

            # regular - simple tactick, shield - if we gonna crush, drift - drift untill speed 0, attack - lets attack enemy, round - vector calculation path
            def getData(self):
                x, y, nx, ny, nd, na = [int(i) for i in input().split()]
                ox, oy = [int(i) for i in input().split()]
                self.player.setParams(x, y)
                self.opponent.setParams(ox, oy)
                self.next_checkpoint_x = nx
                self.next_checkpoint_y = ny
                self.next_checkpoint_angle = na
                self.next_checkpoint_dist = nd

            def _getTactick(self):
                self._current_taktik = "regular"

            def _calculatePathParams(self):
                abs_angle = abs(self.next_checkpoint_angle)
                if abs_angle > 90:
                    thrust = 0
                elif abs_angle > 70:
                    thrust = 25
                elif abs_angle > 45:
                    thrust = 50
                else:
                    thrust = 100

                if self.next_checkpoint_dist > 4000 and (-5 < self.next_checkpoint_angle < 5) and self.boost_not_used:
                    self.boost_not_used = False
                    thrust = "BOOST"
                if self.next_checkpoint_dist < 1000 and abs_angle < 20:
                    thrust = 100
                elif self.next_checkpoint_dist < 3500:
                    if self.player.speed > 600 and abs_angle > 10:
                        thrust = 25
                    elif self.player.speed > 400 and abs_angle > 20:
                        thrust = 50
                    elif self.player.speed > 200 and abs_angle > 30:
                        thrust = 75
                    elif self.player.speed > 50:
                        thrust = 90
                    else:
                        thrust = 100

                        # dist =  calc_distance(self.player.x, self.player.y, self.opponent.x, self.opponent.y)
                # if 600>self.player.speed>300 and dist<1000:
                #    thrust = "SHIELD"
                # print(dist, file=sys.stderr)
                # if self.next_checkpoint_angle==0:
                #    thrust = 100

                return self.path.setPath(self.next_checkpoint_x, self.next_checkpoint_y, thrust)

            def calculatePath(self):
                self._getTactick()
                self._calculatePathParams()

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
