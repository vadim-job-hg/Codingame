import sys
import math

WIDE = 4


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
class Thor:
    tx = 0
    ty = 0
    h = 0
    n = 0
    giants = []

    def __init__(self):
        self.tx, self.ty = [int(i) for i in input().split()]

    def scan(self):
        self.h, self.n = [int(i) for i in input().split()]
        self.giants.clear()
        for i in range(self.n):
            x, y = [int(j) for j in input().split()]
            self.giants.append({'x': x, 'y': y})

    def find_the_middle(self):
        xsumm = ysumm = 0
        for giant in self.giants:
            xsumm += giant['x']
            ysumm += giant['y']
        return int(xsumm / self.n), int(ysumm / self.n)

    def check_if_strike(self):
        for giant in self.giants:
            if abs(self.tx - giant['x']) == 1 or abs(self.ty - giant['y']) == 1:
                return True
        return False

    def move(self):
        dir_x, dir_y = self.find_the_middle()
        if self.check_if_strike():
            action = "STRIKE"
        else:
            action = ''
            if self.ty < dir_y:
                action = action + "S"
                self.ty += 1
            elif self.ty > dir_y:
                action = action + "N"
                self.ty -= 1
            if self.tx < dir_x:
                action = action + "E"
                self.tx += 1
            elif self.tx > dir_x:
                action = action + "W"
                self.tx -= 1
        if action == '':
            action = 'WAIT'
        print(action)


thor = Thor()
while True:
    thor.scan()
    thor.move()

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)
    # print(str(current_x), file=sys.stderr)

