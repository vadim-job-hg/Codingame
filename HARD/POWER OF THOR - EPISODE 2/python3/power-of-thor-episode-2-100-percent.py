# based on https://github.com/texus/codingame/blob/master/SingePlayer/Hard/Thor%20VS%20Giants.cpp
import sys
import math

WIDE = 4


class Thor:
    tx = 0
    ty = 0
    h = 0
    n = 0
    giants = []
    closest_giants = []
    action = "STRIKE"

    def __init__(self):
        self.tx, self.ty = [int(i) for i in input().split()]

    def scan(self):
        self.h, self.n = [int(i) for i in input().split()]
        self.giants.clear()
        for i in range(self.n):
            x, y = [int(j) for j in input().split()]
            self.giants.append({'x': x, 'y': y})

    def find_center(self):
        centerX = centerY = 0
        for giant in self.giants:
            centerX += giant['x']
            centerY += giant['y']

        centerX /= len(self.giants)
        centerY /= len(self.giants)

        return [centerX, centerY]

    def _closest(self):
        self.closest_giants.clear()
        for giant in self.giants:
            if ((abs(giant['x'] - self.tx) <= WIDE) and (abs(giant['y'] - self.ty) <= WIDE)):
                self.closest_giants.append(giant)

    def giants_too_close(self, x, y):
        for giant in self.giants:
            if ((abs(giant['x'] - x) <= 1) and (abs(giant['y'] - y) <= 1)):
                return True
        return False

    def find_move(self, cx, cy):
        if (cx > self.tx):
            if (cy > self.ty):
                self.tx += 1
                self.ty += 1
                self.action = "SE"

            elif (cy < self.ty):
                self.tx += 1
                self.ty -= 1
                self.action = "NE"

            else:
                self.tx += 1
                self.action = "E"
        elif (cx < self.tx):
            if (cy > self.ty):
                self.tx -= 1
                self.ty += 1
                self.action = "SW"
            elif (cy < self.ty):
                self.tx -= 1
                self.ty -= 1
                self.action = "NW"
            else:
                self.tx -= 1
                self.action = "W"
        else:
            if (cy > self.ty):
                self.ty += 1
                self.action = "S"
            elif (cy < self.ty):
                self.ty -= 1
                self.action = "N"
            else:
                self.action = "WAIT"

    def dist(self, first, second):
        return abs(first[0] - second[0]) + abs(first[1] - second[1])

    def _run_away(self):
        profit = {}
        len_closest_giants = len(self.closest_giants)
        if self.tx > 0:
            x = self.tx - 1
            y = self.ty
            if not (self.giants_too_close(x, y)):
                profit["W"] = [len_closest_giants, [x, y]]

        if self.ty > 0:
            x = self.tx
            y = self.ty - 1
            if not (self.giants_too_close(x, y)):
                profit["N"] = [len_closest_giants, [x, y]]

        if self.tx < 40:
            x = self.tx + 1
            y = self.ty
            if (not (self.giants_too_close(x, y))):
                profit["E"] = [len_closest_giants, [x, y]]

        if self.ty < 18:
            x = self.tx
            y = self.ty + 1
            if not (self.giants_too_close(x, y)):
                profit["S"] = [len_closest_giants, [x, y]]

        if (self.tx > 0) and (self.ty > 0):
            x = self.tx - 1
            y = self.ty - 1
            if not (self.giants_too_close(x, y)):
                profit["NW"] = [len_closest_giants, [x, y]]

        if (self.tx < 40) and (self.ty > 0):
            x = self.tx + 1
            y = self.ty - 1
            if not (self.giants_too_close(x, y)):
                profit["NE"] = [len_closest_giants, [x, y]]

        if (self.tx > 0) and (self.ty > 0):
            x = self.tx - 1
            y = self.ty - 1
            if not (self.giants_too_close(x, y)):
                profit["SW"] = [len_closest_giants, [x, y]]

        if (self.tx < 40) and (self.ty < 18):
            x = self.tx + 1
            y = self.ty + 1
            if not (self.giants_too_close(x, y)):
                profit["SE"] = [len_closest_giants, [x, y]]

        self.action = "STRIKE"
        bestOption = [0, [0, 0]]
        bestDist = 0
        center = self.find_center()
        for action, option in profit.items():
            if ((option[0] > bestOption[0]) or ((option[0] == bestOption[0]) and (self.dist(option[1], center) > bestDist))):
                bestOption = option
                move = action
                bestDist = self.dist(bestOption[1], center)

        if self.action != "STRIKE":
            self.tx = bestOption[0]
            self.ty = bestOption[1]

    def _find_best_move(self):
        centerX, centerY = self.find_center()
        if (not (self.giants_too_close(self.tx, self.ty))):
            self.find_move(centerX, centerY)
        else:
            self._run_away()

    def move(self):
        self._closest()
        if len(self.giants) == len(self.closest_giants):
            self.action = "STRIKE"
            print(self.action*3, file=sys.stderr)
        else:
            self._find_best_move()
        print(self.action)


thor = Thor()
while True:
    thor.scan()
    thor.move()