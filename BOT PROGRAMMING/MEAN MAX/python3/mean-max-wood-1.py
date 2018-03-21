import math
import sys


class Wreck:
    def __init__(self, ident, x_pos, y_pos, r, extra):
        self.ident = ident
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.r = r
        self.extra = extra


class Vehicle:
    def __init__(self, ident, x_pos, y_pos, x_vel, y_vel, r, m, extra):
        self.ident = ident
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.r = r
        self.m = m
        # amount of water in the tanker
        self.extra = extra


class Pool:
    def __init__(self, ident, x_pos, y_pos, r, ):
        self.ident = ident
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.r = r


def dist(x1, y1, x2, y2):
    # Euclidean distance
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


past_error = [0, 0]


def position_PID(req_position, actual_position, past_e):
    """
    Give inputs as tuples (x, y).
    """

    kp = 1.5
    ki = 0.5
    kd = 0.01

    e_x = req_position[0] - actual_position[0]
    p_x = kp * e_x
    i_x = ki * (e_x + past_e[0])
    d_x = kd * (e_x - past_e[0])

    e_y = req_position[1] - actual_position[1]
    p_y = kp * e_y
    i_y = ki * (e_y + past_e[1])
    d_y = kd * (e_y - past_e[1])

    new_e_x = p_x + i_x + d_x
    new_e_y = p_y + i_y + d_y
    return (int(new_e_x), int(new_e_y))


angle = 0
# game loop
while True:
    my_score = int(input())
    enemy_score_1 = int(input())
    enemy_score_2 = int(input())
    my_rage = int(input())
    enemy_rage_1 = int(input())
    enemy_rage_2 = int(input())
    # units
    unit_count = int(input())

    # create units
    my_reapers = []
    my_destroyers = []
    my_doofs = []

    tankers = []
    wrecks = []
    pools = []
    # get inputs for the turn
    for i in range(unit_count):
        unit_id, unit_type, player, mass, radius, x, y, vx, vy, extra, \
        extra_2 = input().split()

        unit_id = int(unit_id)
        unit_type = int(unit_type)
        player = int(player)
        mass = float(mass)
        radius = int(radius)
        x = int(x)
        y = int(y)
        vx = int(vx)
        vy = int(vy)
        extra = int(extra)
        extra_2 = int(extra_2)

        if unit_type == 0 and player == 0:
            my_reapers.append(Vehicle(unit_id, x, y, vx, vy, radius, mass, extra))
        elif unit_type == 1 and player == 0:
            my_destroyers.append(Vehicle(unit_id, x, y, vx, vy, radius, mass, extra))
        elif unit_type == 2 and player == 0:
            my_doofs.append(Vehicle(unit_id, x, y, vx, vy, radius, mass, extra))
        elif unit_type == 3:
            tankers.append(Vehicle(unit_id, x, y, vx, vy, radius, mass, extra))
        elif unit_type == 4:
            wrecks.append(Wreck(unit_id, x, y, radius, extra))
        elif unit_type == 6:
            pools.append(Pool(unit_id, x, y, radius))

    ####################################################################
    closest_wreck_dist = 6000
    closest_wreck_pos = [my_destroyers[0].x_pos, my_destroyers[0].y_pos]
    closest_tanker_dist = 6000
    closest_tanker_pos = [0, 0]
    # print(my_reapers, file=sys.stderr)
    # print(my_destroyers, file=sys.stderr)

    # if there are wrecks in the field
    if wrecks:
        for wr in wrecks:
            allow = 1
            for pool in pools:
                if abs(wr.x_pos - pool.x_pos) > 5 and \
                        abs(wr.y_pos - pool.y_pos) > 5:
                    allow = 0

                    # if wreck has 5 or more units of water
            if wr.extra >= 2 and allow:
                min_dist = dist(my_reapers[0].x_pos, my_reapers[0].y_pos,
                                wr.x_pos, wr.y_pos)

                # print(wr.ident, int(min_dist), file=sys.stderr)

                if min_dist < closest_wreck_dist:
                    closest_wreck_dist = min_dist
                    closest_wreck_pos = [wr.x_pos, wr.y_pos, wr.ident]

    # if there are tankers in the field
    if tankers:
        for tank in tankers:
            # if the amount of water in the tanker is greater than 5
            if tank.extra >= 2 and abs(tank.x_pos) < 5500 and abs(tank.y_pos) < 5500:
                min_dist = dist(my_destroyers[0].x_pos,
                                my_destroyers[0].y_pos,
                                tank.x_pos, tank.y_pos)

                # print(tank.ident, int(min_dist), file=sys.stderr)
                if min_dist < closest_tanker_dist:
                    closest_tanker_dist = min_dist
                    closest_tanker_pos = [tank.x_pos, tank.y_pos,
                                          tank.ident]

    if my_doofs:
        r = 6500

        for doof in my_doofs:
            # find point in in the circle to ride to
            k = 1 / (1 + (doof.y_pos / doof.x_pos) ** 2)
            c_x = math.sqrt(r ** 2 * (1 / (1 + k)))
            c_y = math.sqrt(r ** 2 * (1 - (1 / (1 + k))))

            print(int(c_x), int(c_y), file=sys.stderr)

    angle += 0.15
    print(int(closest_wreck_pos[0] - my_reapers[0].x_vel),
          int(closest_wreck_pos[1] - my_reapers[0].y_vel), 300)

    # if my_rage > 200 and int(dist(my_destroyers[0].x_pos,
    #                               my_destroyers[0].y_pos,
    #                               closest_tanker_pos[0],
    #                               closest_tanker_pos[1])) < 2000 \
    #                               and \
    #   closest_tanker_pos[0] != 0 and closest_tanker_pos[1] != 0:

    #     print('SKILL', closest_tanker_pos[0], closest_tanker_pos[1])

    if my_rage > 200 and int(dist(my_destroyers[0].x_pos,
                                  my_destroyers[0].y_pos,
                                  my_reapers[0].x_pos,
                                  my_reapers[0].y_pos)) < 2000:
        print('SKILL', my_reapers[0].x_pos, my_reapers[0].y_pos)
    else:
        print(closest_tanker_pos[0], closest_tanker_pos[1], 300)

    print(int(c_x * math.cos(angle)), int(c_y * math.sin(angle)), 300)

# To debug: print("Debug messages...", file=sys.stderr)