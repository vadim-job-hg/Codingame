# https://www.codingame.com/ide/puzzle/bender-episode-1
import sys
import math


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
class Action:
    DIR_RULES = {'WEST': {'y': 0, 'x': -1}, 'EAST': {'y': 0, 'x': 1}, 'SOUTH': {'y': 1, 'x': 0},
                 'NORTH': {'y': -1, 'x': 0}}
    DIR_CODES = {"S": "SOUTH", "E": "EAST", "N": "NORTH", "W": "WEST"}
    wall_directions = ["SOUTH", "EAST", "NORTH", "WEST"]
    _map = []
    _bender_x = 0
    _bender_y = 0
    _bender_d = 'SOUTH'
    _bender_is_drunk = False
    _teleports = {}

    def __init__(self):
        teleports = []
        l, c = [int(i) for i in input().split()]
        for i in range(l):
            row = list(input())
            try:
                x = row.index("@")
                self._bender_x = x
                self._bender_y = i
            except ValueError:
                pass
            try:
                x = row.index("T")
                teleports.append([x, i])
            except ValueError:
                pass
            self._map.append(row)
            print(row, file=sys.stderr)
            if len(teleports) > 1:
                self._teleports[str(teleports[0][0]) + str(teleports[0][1])] = {'x': teleports[1][0],
                                                                                'y': teleports[1][1]}
                self._teleports[str(teleports[1][0]) + str(teleports[1][1])] = {'x': teleports[0][0],
                                                                                'y': teleports[0][1]}
            print(self._bender_x, self._bender_y, file=sys.stderr)

    def is_next_wall(self):
        return self._map[self._bender_y + self.DIR_RULES[self._bender_d]['y']][
                   self._bender_x + self.DIR_RULES[self._bender_d]['x']] == "#"

    def is_next_x(self):
        return not (self._bender_is_drunk) and self._map[self._bender_y + self.DIR_RULES[self._bender_d]['y']][
                                                   self._bender_x + self.DIR_RULES[self._bender_d]['x']] == "X"

    def _calculate_direction(self):
        current = self._map[self._bender_y][self._bender_x]
        if (current == "$"):
            return False
        elif current in ["S", "N", "E", "W"]:
            self._bender_d = self.DIR_CODES[current]
        elif current == "X":
            self._map[self._bender_y][self._bender_x] = " "
        elif current == "B":
            self._bender_is_drunk = not (self._bender_is_drunk)
        elif current == "I":
            self.wall_directions.reverse()
        elif current == "T":
            coor = self._teleports[str(self._bender_x) + str(self._bender_y)]
            self._bender_x, self._bender_y = coor['x'], coor['y']

        if self.is_next_wall() or self.is_next_x():
            print("WALL ON {0}".format(self._bender_d), file=sys.stderr)
            for direction in self.wall_directions:
                self._bender_d = direction
                if not (self.is_next_wall() or self.is_next_x()):
                    break
                print("WALL ON {0}".format(self._bender_d), file=sys.stderr)

                return True

    def _move(self):
        self._bender_y += self.DIR_RULES[self._bender_d]['y']
        self._bender_x += self.DIR_RULES[self._bender_d]['x']
        return self._bender_d

    def run(self):
        strings = []
        while self._calculate_direction():
            strings.append(self._move())
            if (len(strings)) > 10000:
                print("LOOP")
                return False
        for str1 in strings:
            print(str1)
        return True

# Write an action using print
# To debug: print("Debug messages...", file=sys.stderr)
act = Action()
act.run()
