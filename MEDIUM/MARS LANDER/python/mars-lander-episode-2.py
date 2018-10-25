import sys
import math

GRAV = 3.711
POD_RADIUS = 5
MAX_VSPEED_LANDING = 40
MAX_HSPEED_LANDING = 20
MAX_POWER = 4
MAX_ANGLE = 90
DANGER_LANDING_ANGLE = 30
FAST_LANDING_ANGLE = 45


# a = d(v)/d(t)
class Shutle():
    angle = 0
    power = 0
    v_speed = 0
    h_speed = 0
    v_a = 0
    h_a = 0

    def getParams(self):
        v_speed_last, h_speed_last = self.v_speed, self.h_speed
        self.x, self.y, self.h_speed, self.v_speed, self.fuel, self.rotate, self.power = [int(i) for i in
                                                                                          raw_input().split()]
        self.v_a, self.h_a = (self.v_speed - v_speed_last), (self.h_speed - h_speed_last)

    def printParams(self):
        print("{0} {1}".format(self.angle, self.power))


class LandingZone():
    _landing_start = 0
    _landing_end = 7000
    _landing_height = 0
    _shutle = Shutle()
    _dir_mult = 0
    _hightest_dot = 0

    def __init__(self):
        surface_n = int(raw_input())
        land_x_prev = land_y_prev = 0
        for i in range(surface_n):
            land_x, land_y = [int(j) for j in raw_input().split()]
            if (land_x_prev != 0 and land_y_prev == land_y):
                self._landing_height = land_y
                self._landing_start = land_x_prev
                self._landing_end = land_x
            if self._hightest_dot < land_y:
                self._hightest_dot = land_y
            land_x_prev, land_y_prev = land_x, land_y

    def getShutleSituation(self):
        self._shutle.getParams()
        if self._landing_start < self._shutle.x < self._landing_end:
            self._dir_mult = 0
        elif self._shutle.x < self._landing_start:
            self._dir_mult = - 1
        else:
            self._dir_mult = 1

    def getToSafeZone(self):
        if self._dir_mult != 0:
            if self._shutle.y - self._hightest_dot < 500:
                l_a = DANGER_LANDING_ANGLE
                l_s = MAX_HSPEED_LANDING
            else:
                l_a = FAST_LANDING_ANGLE
                l_s = MAX_HSPEED_LANDING * 2
            self._shutle.power = 4
            if ((-self._dir_mult * self._shutle.h_speed) < l_s):
                self._shutle.angle = int(self._dir_mult * l_a)
            elif (-self._dir_mult * self._shutle.h_speed > l_s + 5):
                self._shutle.angle = -int(self._dir_mult * l_a)
            else:
                self._shutle.angle = 0
        else:
            self.gorisontalCorrect()

    def gorisontalCorrect(self):
        if abs(self._shutle.h_speed) > MAX_HSPEED_LANDING or (
                self._shutle.h_speed > 0 and self._landing_end - self._shutle.x < 500) or (
                self._shutle.h_speed < 0 and self._landing_start - self._shutle.x < -500):
            self._shutle.angle = self._shutle.h_speed * 3
            if self._shutle.angle > DANGER_LANDING_ANGLE:
                self._shutle.angle = DANGER_LANDING_ANGLE
            elif self._shutle.angle < -DANGER_LANDING_ANGLE:
                self._shutle.angle = -DANGER_LANDING_ANGLE
        else:
            self._shutle.angle = 0

    def landing(self):
        if (self._shutle.v_speed < -(
            MAX_VSPEED_LANDING - 5) or self._shutle.angle != 0 or self._dir_mult != 0) and self._shutle.y < 2800:
            self._shutle.power = 4
        else:
            self._shutle.power = 3

    def run(self):
        self.getToSafeZone()
        self.landing()
        self._shutle.printParams()


landing_zone = LandingZone()
while True:
    landing_zone.getShutleSituation()
    landing_zone.run()
