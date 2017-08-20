import sys
import math
import copy


class Action:
    STATUS_SEARCH = 'status_search'
    STATUS_RETURN = 'status_return'
    BACK_DIRECTION = {'LEFT': 'RIGHT', 'RIGHT': 'LEFT', 'UP': 'DOWN', 'DOWN': 'UP'}
    NEXT_DIRECTIONL = {'RIGHT': 'UP', 'UP': 'LEFT', 'LEFT': 'DOWN', 'DOWN': 'RIGHT'}
    NEXT_DIRECTIONR = {'RIGHT': 'DOWN', 'UP': 'RIGHT', 'LEFT': 'UP', 'DOWN': 'LEFT'}
    NEXT_POSITION = {'LEFT': {'rows': 0, 'cols': -1}, 'RIGHT': {'rows': 0, 'cols': 1}, 'UP': {'rows': -1, 'cols': 0},
                     'DOWN': {'rows': 1, 'cols': 0}}
    cols = 0
    rows = 0
    countdown = 0
    kirk = {'r': 0, 'c': 0}
    renember = {}
    status = None
    map = []
    direction = 'RIGHT'

    def __init__(self):
        self.status = self.STATUS_SEARCH
        self.rows, self.cols, self.countdown = [int(i) for i in input().split()]

    def scan(self):
        self.kirk['r'], self.kirk['c'] = [int(i) for i in input().split()]
        self.map.clear()
        for i in range(self.rows):
            self.map.append(list(input()))

    def get_next(self):
        return self.map[self.kirk['r'] + self.NEXT_POSITION[self.direction]['rows']][
            self.kirk['c'] + self.NEXT_POSITION[self.direction]['cols']]

    def touch_right_wall(self):
        self.direction = self.NEXT_DIRECTIONL[self.direction]
        while self.get_next() == '#':
            self.direction = self.NEXT_DIRECTIONR[self.direction]

    def save_direction(self):
        self.renember[self.kirk['c'] + self.kirk['r'] * self.cols] = self.direction

    def get_direction(self):
        if (self.map[self.kirk['r']][self.kirk['c']] == 'C'):
            self.save_direction()
            self.status = self.STATUS_RETURN
            self.direction = self.BACK_DIRECTION[self.direction]
        elif self.status is self.STATUS_SEARCH:
            self.save_direction()
            self.touch_right_wall()
        else:
            self.direction = self.BACK_DIRECTION[self.renember[self.kirk['c'] + self.kirk['r'] * self.cols]]

    def run(self):
        print(self.direction)


act = Action()
while True:
    act.scan()
    act.get_direction()
    act.run()