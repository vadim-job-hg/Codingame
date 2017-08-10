import sys
import math

WIDTH = 16000
HEIGHT = 9000
ASH_SPEED = 1000
ZOMBIE_SPEED = 400
ASH_ATTACK_DISTANCE = 2000
ZOMBIE_ATTACK_DISTANCE = 400


# TODO:  MOVE WITH VECTORS? USE ZOMBIE SPEED
class Action:
    x = y = None
    humans = {}
    zombies = {}

    def __init__(self):
        pass

    def read_situation(self):
        self.x, self.y = [int(i) for i in input().split()]
        human_count = int(input())
        self.humans.clear()
        for i in range(human_count):
            human_id, human_x, human_y = [int(j) for j in input().split()]
            self.humans[human_id] = {'x': human_x, 'y': human_y}
        self.zombies.clear()
        zombie_count = int(input())
        for i in range(zombie_count):
            zombie_id, zombie_x, zombie_y, zombie_xnext, zombie_ynext = [int(j) for j in input().split()]
            self.humans[zombie_id] = {'x': zombie_x, 'y': zombie_y, 'xn': zombie_xnext, 'yn': zombie_ynext}


act = Action
while True:
    act.read_situation()

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)

    # Your destination coordinates
    print("0 0")
