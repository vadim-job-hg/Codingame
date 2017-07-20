import sys
import math
import numpy as np


def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm


def angle_between(v1, v2):
    v1_u = normalize(v1)
    v2_u = normalize(v2)
    angle = np.arccos(np.dot(v1_u, v2_u))
    if np.isnan(angle):
        if (v1_u == v2_u).all():
            return 0.0
        else:
            return np.pi
    return angle


def angle_between_ori(v1):
    angle = np.arccos(abs(v1[0]) / np.linalg.norm(v1))

    if v1[0] >= 0 and v1[1] >= 0:
        return angle
    elif v1[0] >= 0 and v1[1] < 0:
        return 2 * np.pi - angle
    elif v1[0] < 0 and v1[1] >= 0:
        return np.pi - angle
    elif v1[0] < 0 and v1[1] < 0:
        return angle + np.pi


def eval_next_pos(cur_co, dest_co, v, power):
    v_target = dest_co - cur_co
    norm_power = v_target * power / np.linalg.norm(v_target)
    next_co = cur_co + v + norm_power
    angle = np.round(np.degrees(angle_between_ori(v_target)))
    next_co = np.around(next_co)
    next_v = (v + norm_power) * 0.85
    next_v = np.trunc(next_v)

    return next_co, next_v, angle


def predict_pos(cur_co, dest_co, v, power, turn_num):  # thrus = 0 and dest cst
    nc = cur_co
    nv = v
    ang = 0
    for i in range(turn_num):
        nc, nv, ang = eval_next_pos(nc, dest_co, nv, power)

    return nc, nv, ang


# ret dest,done
def check_good_orientation(bot_param, dest):
    if bot_param["angle"] == -1:
        return True  # au debut on fait ce qu'on veut
    else:
        obj_ang = np.degrees(angle_between_ori(dest - bot_param["co"]))  # new angle if we turn the bot

        if min(np.ceil(abs(bot_param["angle"] - obj_ang)), np.ceil(360 - abs(bot_param["angle"] - obj_ang))) > 18:
            return False
        else:
            return True


def circle_intersect(seg_a, seg_b, circ_pos):
    seg_v = seg_b - seg_a

    pt_v = circ_pos - seg_a

    if np.linalg.norm(seg_v) == 0:
        return False

    if np.dot(seg_v, seg_v) <= 0:
        print(" *** inf0 ", file=sys.stderr)

        seg_v_unit = normalize(seg_v)
        proj = np.dot(pt_v, seg_v_unit)

        closest = 0
        if proj <= 0:
            closest = seg_a
        elif proj >= np.linalg.norm(seg_v):  # seg_v.len():
            closest = seg_b
        else:
            proj_v = seg_v_unit * proj
            closest = proj_v + seg_a

        dist_v = circ_pos - closest  # minimum distance between circle and segment

        if np.linalg.norm(dist_v) < 600:  # checkpoint 600
            return True  # intersection
        else:
            return False

    def find_accel_until(bot_param, dest_co_, power, max_test):
        # return coord final and angle final (at the end of the loop)
        coord = bot_param["co"].copy()
        speed = bot_param["speed"].copy()
        dest_co = dest_co_.copy()

        ang = 0
        prev_ang = bot_param["angle"]

        warning_angle = False

        list_coord = []  # list holds all the coord/speed computed

        intersect = (False, 0)

        for i in range(max_test):  # 100 max for a turn
            n_coord, speed, ang = eval_next_pos(coord, dest_co, speed, power)

            # if prev_ang !=0:
            if min(np.ceil(abs(prev_ang - ang)), np.ceil((360 - abs(prev_ang - ang)))) > 18:
                print("** warning angle ", file=sys.stderr)
                warning_angle = True

            prev_ang = ang

            if circle_intersect(coord, n_coord, dest_co):
                intersect = (True, i)
                coord = n_coord
                break

            list_coord.insert(0, (n_coord, speed, ang))
            coord = n_coord

        return intersect[0], intersect[1], coord, ang, list_coord, warning_angle  # target angle (return a vector)

    def find_how_much_zero(l, dest_co, step):
        # dest_co = dest_co_.copy()

        ret_list = []
        found = False
        # list inversé, d'ou ca marchce
        for coord, speed, _ in l[0:10]:  # on garde que les 4 premiers
            for i in range(7):  # 100 max for a turn
                n_coord, speed, ang = eval_next_pos(coord, dest_co, speed, 0)

                # if np.norm(dest_co-coord) > np.norm(dest_co-n_coord):


                if circle_intersect(coord, n_coord, dest_co):
                    ret_list.append((i, speed))
                    coord = n_coord
                    found = True
                    break

                coord = n_coord

        return found, ret_list

    def compute_step_angle(coord, cur_ang, dest_obj):  # how much step we need ?
        target_angle = np.degrees(angle_between_ori(dest_obj - coord))

        step = min(np.ceil(abs(cur_ang - target_angle) / 18), np.ceil((360 - abs(cur_ang - target_angle)) / 18))

        return step

    def coord_str(co):
        # print(co, file=sys.stderr)
        # return "100 100"
        return "{:d} {:d}".format(int(co[0]), int(co[1]))

    def print_action(coord, thrust, string):
        print(coord_str(coord), " ", thrust, " ", string)

    checkpoints = {}
    my_bots = {}
    adv_bots = {}

    # phase
    previous_state = {}
    previous_state["phase"] = 1
    previous_state["ck"] = 0

    laps = int(input())
    checkpoint_count = int(input())
    for i in range(checkpoint_count):
        checkpoint_x, checkpoint_y = [int(j) for j in input().split()]
        checkpoints[i] = np.array([checkpoint_x, checkpoint_y])

    # game loop
    while True:
        for i in range(2):
            x, y, vx, vy, angle, ncp = [int(j) for j in input().split()]
            bot = {}
            bot["co"] = np.array([x, y])
            bot["speed"] = np.array([vx, vy])
            bot["angle"] = angle
            bot["ncp"] = ncp
            my_bots[i] = bot
        for i in range(2):
            x, y, vx, vy, angle, ncp = [int(j) for j in input().split()]
            bot = {}
            bot["co"] = np.array([x, y])
            bot["speed"] = np.array([vx, vy])
            bot["angle"] = angle
            bot["ncp"] = ncp
            adv_bots[i] = bot

        # Write an action using print
        # To debug: print("Debug messages...", file=sys.stderr)



        state = {}
        # *** FIND IN WHICH PHASE WE ARE ***


        if previous_state["phase"] == 1:
            # OK step 1, check orientation
            if check_good_orientation(my_bots[0],
                                      checkpoints[my_bots[0]["ncp"]]):
                state["phase"] = 2  # OK we can speed
                state["speed2"] = 200
            else:
                state["phase"] = 1  # still in phase 1 since no orientation

            state["ck"] = my_bots[0]["ncp"]
        elif previous_state["phase"] == 2:

            if previous_state["ck"] != my_bots[0]["ncp"]:  # ck change, phase 1 !
                state["phase"] = 1
                state["ck"] = my_bots[0]["ncp"]
            else:
                step = 0
                step_pred = 0
                co_pred = 0
                ang_pred = 0
                # compute different solutions based on different accel

                min_step = 9999
                found_min = False
                for accele in [200, 140, 70, 20]:

                    found, step_pred, co_pred, ang_pred, l, wa = find_accel_until(my_bots[0],
                                                                                  checkpoints[my_bots[0]["ncp"]],
                                                                                  accele,
                                                                                  100)

                    # ok warning angle act
                    # if waring angle set, means we are too fast


                    print("Accel tested ", accele, " step pred ", step_pred, file=sys.stderr)

                    if not wa:
                        if step < min_step:
                            state["speed2"] = accele
                            min_step = step
                            found_min = True
                            # break

                if not found_min:
                    # hot hot !
                    state["speed2"] = 0
                # how much step to turn the pod to target the next checpoint
                step = compute_step_angle(co_pred,
                                          ang_pred,
                                          checkpoints[(my_bots[0]["ncp"] + 1) % checkpoint_count])

                print("Step :", step, " step pred : ", step_pred, file=sys.stderr)






                if step_pred > 4 or step < 4:
                    # ok we have still time to turn, still phase 2
                    state["phase"] = 2
                else:
                    # need to turn !
                    state["phase"] = 3
                    state["steps"] = int(step)
                    state["coord_pred"] = co_pred
                    state["ck"] = my_bots[0]["ncp"]

                state["ck"] = my_bots[0]["ncp"]

        elif previous_state["phase"] == 3:
            if previous_state["ck"] < my_bots[0]["ncp"]:
                # the checkpoint is passed, phase 4 (i.e phase 1) !
                state["phase"] = 1
            else:
                found, step_pred, co_pred, ang_pred, l, _ = find_accel_until(my_bots[0],
                                                                             checkpoints[my_bots[0]["ncp"]],
                                                                             0,
                                                                             previous_state["steps"] + 6)

                print("p3 -step ", step_pred, found, file=sys.stderr)
                # print(found,file=sys.stderr)
                if not found:
                    # ok not found, perhaps collision ?
                    # return to step 1
                    state["phase"] = 1  # different from previous condition because "ncp" was not updated
                else:
                    state["phase"] = 3  # still phase 3
                    state["coord_pred"] = co_pred
                    state["ck"] = my_bots[0]["ncp"]
                    state["steps"] = int(step_pred)

        # *** FIND THE RIGHT ACTION ACORDING TO THE PHASE ***




        if state["phase"] == 1:
            # we turn with np power
            print_action(checkpoints[my_bots[0]["ncp"]], 0, "S1")
        elif state["phase"] == 2:
            # ok on tartine
            print_action(checkpoints[my_bots[0]["ncp"]], state["speed2"], "S2")
        elif state["phase"] == 3:
            # we need to turn the chip with 0 accel
            # find how much we turn
            coord_obj = checkpoints[(my_bots[0]["ncp"] + 1) % checkpoint_count]

            trans_vector = coord_obj - state["coord_pred"]

            trans_vector = normalize(trans_vector) * 10
            orient_coord = trans_vector + my_bots[0]["co"]

            orient_coord = np.around(orient_coord)

            print(
            "-- obj", coord_obj, "co_p", state["coord_pred"], "tv ", trans_vector, "oc ", orient_coord, file=sys.stderr)
            print(my_bots[0]["co"], file=sys.stderr)
            print_action(orient_coord, 0, "S3")

        print_action(adv_bots[0]["co"], 100, "")

        # print(coord_str(checkpoints[0]) + " 200")
        # print(coord_str(checkpoints[0]) + " 0")
        previous_state = state
