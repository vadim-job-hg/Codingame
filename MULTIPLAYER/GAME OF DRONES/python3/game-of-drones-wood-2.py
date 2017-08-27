import sys
import math

WIDTH = 4000
HEIGHT = 1800


class Act:
    zones = []

    def __init__(self):
        # p: number of players in the game (2 to 4 players)
        # id: ID of your player (0, 1, 2, or 3)
        # d: number of drones in each team (3 to 11)
        # z: number of zones on the map (4 to 8)
        self.p, self.id, self.d, self.z = [int(i) for i in input().split()]
        for i in range(self.z):
            x, y = [int(j) for j in input().split()]
            self.zones.append({'x': x, 'y': y})

    def scan(self):
        for i in range(self.z):
            tid = int(
                input())  # ID of the team controlling the zone (0, 1, 2, or 3) or -1 if it is not controlled. The zones are given in the same order as in the initialization.
        for i in range(self.p):
            for j in range(self.d):
                # dx: The first D lines contain the coordinates of drones of a player with the ID 0, the following D lines those of the drones of player 1, and thus it continues until the last player.
                dx, dy = [int(k) for k in input().split()]

    def run(self):
        for i in range(1, self.d + 1):
            zone = self.zones[(i + self.z) % self.z]
            # Write an action using print
            # To debug: print("Debug messages...", file=sys.stderr)
            # output a destination point to be reached by one of your drones. The first line corresponds to the first of your drones that you were provided as input, the next to the second, etc.
            print("{0} {1}".format(zone['x'], zone['y']))


act = Act()
while True:
    act.scan()
    act.run()

