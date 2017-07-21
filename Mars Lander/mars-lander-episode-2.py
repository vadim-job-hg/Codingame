import sys
import math

GRAV = 3.711
POD_RADIUS = 5
MAX_VSPEED_LANDING = 40
MAX_HSPEED_LANDING = 20


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
class Shutle():
    angle = 0
    power = 0

    def getParams(self):
        self.x, self.y, self.h_speed, self.v_speed, self.fuel, self.rotate, self.power = [int(i) for i in
                                                                                          input().split()]

    def printParams(self):
        print("{0} {1}".format(self.angle, self.power))


class LandingZone():
    _landing_start = 0
    _landing_end = 7000
    _landing_height = 0
    _shutle = Shutle()
    _step = 1

    def __init__(self):
        surface_n = int(input())
        land_x_prev = land_y_prev = 0
        for i in range(surface_n):
            land_x, land_y = [int(j) for j in input().split()]
            if (land_x_prev != 0 and land_y_prev == land_y):
                self._landing_height = land_y
                self._landing_start = land_x_prev
                self._landing_end = land_x
            land_x_prev, land_y_prev = land_x, land_y
        print("Start: " + str(self._landing_start), file=sys.stderr)
        print("End: " + str(self._landing_end), file=sys.stderr)
        print("Height: " + str(self._landing_height), file=sys.stderr)

        def getShutleSituation(self):
            self._shutle.getParams()

        def getToSafeZone(self):
            if self._landing_start < self._shutle.x < self._landing_end:
                self.gorisontalCorrect()
                self.landing()
            else:
                if self._shutle.x < self._landing_start:
                    vdistance = self._landing_start - self._shutle.x
                    ang_mn = - 1
                else:
                    vdistance = self._shutle.x - self._landing_end
                    ang_mn = 1
                print(self._shutle.h_speed, file=sys.stderr)
                self._shutle.power = 4
                if ((-ang_mn * self._shutle.h_speed) < MAX_HSPEED_LANDING * 2):
                    self._shutle.angle = int(ang_mn * 45)
                elif (-ang_mn * self._shutle.h_speed > MAX_HSPEED_LANDING * 2 + 5):
                    self._shutle.angle = -int(ang_mn * 45)
                else:
                    self._shutle.angle = 0

        def gorisontalCorrect(self):
            if self._shutle.v_speed == 0:
                self._shutle.angle = 0
            else:
                print(self._shutle.h_speed, file=sys.stderr)
                self._shutle.angle = self._shutle.h_speed * 3
                if self._shutle.angle > 45:
                    self._shutle.angle = 45
                elif self._shutle.angle < -45:
                    self._shutle.angle = -45

        def landing(self):
            if self._shutle.v_speed < -(MAX_VSPEED_LANDING - 5):
                self._shutle.power = 4
            else:
                self._shutle.power = 3

        def run(self):
            self.getToSafeZone()
            self._shutle.printParams()

    landing_zone = LandingZone()
    while True:
        landing_zone.getShutleSituation()
        landing_zone.run()
        pass
