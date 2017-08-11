import sys
import math

WIDTH = 16000
HEIGHT = 9000
ASH_SPEED = 1000
ZOMBIE_SPEED = 400
ASH_ATTACK_DISTANCE = 2000
ZOMBIE_ATTACK_DISTANCE = 400


def dist(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


# TODO:  MOVE WITH VECTORS? USE ZOMBIE SPEED
class Action:
    x = y = None
    humans = {}
    zombies = {}
    zombie_attack_human = {}

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
            self.zombies[zombie_id] = {'x': zombie_x, 'y': zombie_y, 'xn': zombie_xnext, 'yn': zombie_ynext}
        self.zombie_attack_human.clear()
        for hid, human in self.humans.items():
            for zid, zomb in self.zombies.items():
                if (zomb['xn'] > human['x'] - 600 or zomb['xn'] < human['x'] + 600) and (
                        zomb['yn'] > human['y'] - 600 or zomb['yn'] < human['y'] + 600):
                    self.zombie_attack_human[zid] = hid

    def klaatu_barada_nikhe_khe_khe(self):
        # get best zombie
        zomb = self.get_closest()
        if zomb:
            print(zomb['x'], zomb['y'])

    def get_closest(self):
        distance_to_human = distance_to_hero = WIDTH
        closest_to_human = None
        closes_to_hero = None
        for zid, zomb in self.zombies.items():
            human = self.humans[self.zombie_attack_human[zid]]
            dis = dist(zomb['x'], zomb['y'], human['x'], human['y'])
            hero_distance = dist(self.x, self.y, human['x'], human['y'])
            if distance_to_human > dis and (hero_distance - ASH_ATTACK_DISTANCE) / ASH_SPEED < (
                dis + ZOMBIE_ATTACK_DISTANCE) / ZOMBIE_SPEED:
                distance_to_human = dis
                closest_to_human = zomb
            if distance_to_hero > hero_distance:
                distance_to_hero = hero_distance
                closes_to_hero = zomb
        if closest_to_human:
            return closest_to_human
        else:
            return closes_to_hero


act = Action()
while True:
    act.read_situation()
    act.klaatu_barada_nikhe_khe_khe()
    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)

    # Your destination coordinates

