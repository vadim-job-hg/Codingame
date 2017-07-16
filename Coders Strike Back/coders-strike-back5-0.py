import sys
import math


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
def calc_distance(x, y, x2, y2):
    return math.sqrt(((x2 - x) ** 2) + ((y2 - y) ** 2))

class Path():
    x = None
    y = None
    trust = None

    def __init__(self, x, y, trust):
        self.x = x
        self.y = y
        self.trust = trust

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getTrust(self):
        return self.trust

    def getString(self):
        return "{0} {1} {2}".format(self.x, self.y, self.trust)

class Coordinates():
    pass

class Pod():
    x = None
    y = None
    next_checkpoint_x = None
    next_checkpoint_y = None
    next_checkpoint_angle = 0
    next_checkpoint_dist = 0
    opponent_x = None
    opponent_y = None
    path_points = []

    current_speed = 0
    all_path_point_known = False
    path = None
    def getData(self):
        x, y, nx, ny, nd, na = [int(i) for i in input().split()]
        ox, oy = [int(i) for i in input().split()]
        self.x = x
        self.y = y
        self.next_checkpoint_x = nx
        self.next_checkpoint_y = ny
        self.next_checkpoint_angle = na
        self.next_checkpoint_dist = nd
        self.opponent_x = ox
        self.opponent_y = oy
    def calculateSpeed(self):
        pass

    def getMoveVector(self):
        pass

    def getNextCheckpoint(self):# heckpoint after current
        pass


    def run(self):
        if self.path is not None:
            print(self.path.getString())
        else:
            raise Exception('OOOPS!')


avaliable_boost = True
# game loop
while True:
    # next_checkpoint_x: x position of the next check point
    # next_checkpoint_y: y position of the next check point
    # next_checkpoint_dist: distance to the next checkpoint
    # next_checkpoint_angle: angle between your pod orientation and the direction of the next checkpoint
    x, y, next_checkpoint_x, next_checkpoint_y, next_checkpoint_dist, next_checkpoint_angle = [int(i) for i in
                                                                                               input().split()]
    opponent_x, opponent_y = [int(i) for i in input().split()]

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)
    abs_angle = math.fabs(next_checkpoint_angle)
    if avaliable_boost and next_checkpoint_dist > 5000 and abs_angle < 5:
        trust = 'BOOST'
        avaliable_boost = False
    elif abs_angle > 120:
        trust = str(0)
    elif abs_angle > 90:
        trust = str(15)
    elif next_checkpoint_dist < 3000:
        trust = str(int((1 - abs_angle / 90) * 100))
    elif abs_angle < 45:
        trust = str(100)
    elif abs_angle < 90:
        trust = str(70)
        # You have to output the target position
    # followed by the power (0 <= thrust <= 100)
    # i.e.: "x y thrust"
    print(str(next_checkpoint_x) + " " + str(next_checkpoint_y) + " " + trust)
