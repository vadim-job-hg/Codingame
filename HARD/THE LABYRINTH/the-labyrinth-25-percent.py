import sys
import math

SCAN_RADIUS = 2
BACK_DIRECTION = {'LEFT': 'RIGHT', 'RIGHT': 'LEFT', 'UP': 'DOWN', 'DOWN': 'UP'}
NEXT_DIRECTIONL = {'RIGHT': 'UP', 'UP': 'LEFT', 'LEFT': 'DOWN', 'DOWN': 'RIGHT'}
NEXT_DIRECTIONR = {'RIGHT': 'DOWN', 'UP': 'RIGHT', 'LEFT': 'UP', 'DOWN': 'LEFT'}
NEXT_POSITION = {'LEFT': {'rows': 0, 'cols': -1}, 'RIGHT': {'rows': 0, 'cols': 1}, 'UP': {'rows': -1, 'cols': 0},
                 'DOWN': {'rows': 1, 'cols': 0}}


class Action:
    STATUS_SEARCH = 'status_search'
    STATUS_RETURN = 'status_return'
    cols = 0
    rows = 0
    countdown = 0
    kirk = {'r': 0, 'c': 0}
    move_history = {}
    dead_end = {}
    pos_dir = []
    status = None
    map = []
    direction = 'RIGHT'

    def __init__(self):
        self.status = self.STATUS_SEARCH
        self.rows, self.cols, self.countdown = [int(i) for i in input().split()]
        self.pos_dir

    def scan(self):
        self.kirk['r'], self.kirk['c'] = [int(i) for i in input().split()]
        self.map.clear()
        for i in range(self.rows):
            self.map.append(list(input()))

    def get_next(self):
        return self.map[self.kirk['r'] + NEXT_POSITION[self.direction]['rows']][
            self.kirk['c'] + NEXT_POSITION[self.direction]['cols']]

    def get_by(self, c, r):
        return self.map[r][c]

    def touch_right_wall(self):
        self.direction = NEXT_DIRECTIONL[self.direction]
        while self.get_next() == '#' or self.load_direction(self.kirk['c'] + NEXT_POSITION[self.direction]['cols'],
                                                            self.kirk['r'] + NEXT_POSITION[self.direction][
                                                                'rows']) is not None:
            self.direction = NEXT_DIRECTIONR[self.direction]

    def save_direction(self):
        c = self.kirk['c'] + NEXT_POSITION[self.direction]['cols']
        r = self.kirk['r'] + NEXT_POSITION[self.direction]['rows']
        if self.move_history.get((c, r), None) is None:
            self.move_history[(c, r)] = self.direction

    def load_direction(self, c, r):
        return self.move_history.get((c, r), None)

    def ckeck_deadend(self, minr, minc, maxr, maxc):
        pass

    def can_move(self):
        pass

    def get_direction(self):
        if self.get_by(self.kirk['c'], self.kirk['r']) == 'C':
            self.status = self.STATUS_RETURN

        if self.status == self.STATUS_SEARCH:
            minr = (0, self.kirk['r'] - SCAN_RADIUS)[self.kirk['r'] - SCAN_RADIUS > 0]
            minc = (0, self.kirk['c'] - SCAN_RADIUS)[self.kirk['c'] - SCAN_RADIUS > 0]
            maxr = (self.rows, self.kirk['r'] + SCAN_RADIUS)[self.kirk['r'] + SCAN_RADIUS < self.rows]
            maxc = (self.cols, self.kirk['c'] + SCAN_RADIUS)[self.kirk['c'] + SCAN_RADIUS < self.cols]
            self.ckeck_deadend(minr, minc, maxr, maxc)

            self.touch_right_wall()
            self.save_direction()
        else:
            self.direction = BACK_DIRECTION[self.move_history[(self.kirk['c'], self.kirk['r'])]]

    def run(self):
        print(self.direction)


act = Action()
while True:
    act.scan()
    act.get_direction()
    act.run()