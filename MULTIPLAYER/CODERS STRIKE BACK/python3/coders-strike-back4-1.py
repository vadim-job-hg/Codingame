# THE WHOLE CODE IS FROM
# https://github.com/jmistx/coders-strike-back/blob/master/startegy_1.py
import math

def diff(v1, v2):
    return tuple((a - b) for a, b in zip(v1, v2))


def dotproduct(v1, v2):
    return sum((a * b) for a, b in zip(v1, v2))


def length(v):
    return math.sqrt(dotproduct(v, v))


def angle(v1, v2):
    return math.acos(dotproduct(v1, v2) / (length(v1) * length(v2)))


def to_grad(angle):
    return angle / math.pi * 180
# next_checkpoint_x: x position of the next check point
# next_checkpoint_y: y position of the next check point
# next_checkpoint_dist: distance to the next checkpoint
# next_checkpoint_angle: angle between your pod orientation and the direction of the next checkpoint

# You have to output the target position
# followed by the power (0 <= thrust <= 100)
# i.e.: "x y thrust"

class ExternalState:
    def __init__(self):
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


class InternalState:
    def __init__(self):
        self.checkpoints = []
        self.boost_not_used = True
        self.current_next_checkpoint = None
        self.i_know_checkpoints = False

    def checkpoint_changed(self, new_x, new_y):
        if (new_x, new_y) in self.checkpoints:
            self.i_know_checkpoints = True

    def update_checkpoint(self, x, y):
        if self.current_next_checkpoint is None:
            self.current_next_checkpoint = (x, y)

        if (x, y) != self.current_next_checkpoint:
            self.checkpoint_changed(x, y)
            self.current_next_checkpoint = (x, y)

        if (x, y) not in self.checkpoints:
            self.checkpoints.append((x, y))

    def two_points_in_row(self, es):
        current_point_index = self.checkpoints.index(self.current_next_checkpoint)
        next_point_index = (current_point_index + 1) % len(self.checkpoints)
        next_point = self.checkpoints[next_point_index]
        next_point_vector = diff(next_point, self.current_next_checkpoint)
        next_angle = angle(next_point, self.current_next_checkpoint) / math.pi * 180
        if (-5 < es.next_checkpoint_angle < 5) and (-5 < next_angle < 5):
            return True
        return False


def make_decision(es, si):
    si.update_checkpoint(es.next_checkpoint_x, es.next_checkpoint_y)
    # si.update_opponent(es.opponent_x, es.opponent_y)

    if es.next_checkpoint_angle > 90 or es.next_checkpoint_angle < -90:
        thrust = 0
    else:
        thrust = 100

    if es.next_checkpoint_dist > 7000 and (-5 < es.next_checkpoint_angle < 5) and si.boost_not_used:
        si.boost_not_used = False
        thrust = "BOOST"

    if es.next_checkpoint_dist < 2500:
        thrust = 50

    if es.next_checkpoint_dist < 1000:
        thrust = 100

    # if si.i_know_checkpoints:
    #     if si.two_points_in_row(es):
    #         thrust = 100

    # o = (es.opponent_x, es.opponent_y)
    # m = (es.x, es.y)
    # aim = (es.next_checkpoint_x, es.next_checkpoint_y)
    # my_direction_vector = diff(aim, m)
    # opponent_position_vector = diff(o, m)
    # ln = length(opponent_position_vector)
    # an = to_grad(angle(opponent_position_vector, my_direction_vector))
    # print("o: {0}, m: {1}, df: {2}, ln: {3}, an: {4}".format(o, m, opponent_position_vector, ln, an), file=sys.stderr)
    # if length(diff(o, m)) < 1000 and (-10 < an < 10):
    #     thrust = "SHIELD"

    return es.next_checkpoint_x, es.next_checkpoint_y, thrust


def print_debug(es, si):
    pass

def loop(es, si):
    print_debug(es, si)
    decision = make_decision(es, si)
    print("{0} {1} {2}".format(*decision))


si = InternalState()
# game loop
while True:
    loop(ExternalState(), si)