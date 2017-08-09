# https://www.codingame.com/ide/puzzle/don't-panic-episode-1
import sys
import math

LOWER_FLOOR = LEFTMOST = 0


class LeadClone:
    clone_pos = 0
    clone_floor = 0
    direction = ""
    current_floor = 0

    def getParams(self):
        clone_floor, clone_pos, self.direction = input().split()
        self.clone_floor = int(clone_floor)
        self.clone_pos = int(clone_pos)


class Area:
    elevator_coors = {}

    def isExitHere(self, floor):
        print(floor, self.exit_floor, file=sys.stderr)
        if floor == self.exit_floor:
            return self.exit_pos
        else:
            return None

    def getClosest(self, fl, cpos):
        closest, pos = self.width, 0
        print(closest, pos, self.elevator_coors, file=sys.stderr)
        for floor in self.elevator_coors.get(fl):
            print(floor, file=sys.stderr)
            if closest > abs(floor - cpos):
                closest = abs(floor - cpos)
                pos = floor
        return pos

    def __init__(self):
        self.nb_floors, self.width, self.nb_rounds, self.exit_floor, self.exit_pos, self.nb_total_clones, self.nb_additional_elevators, nb_elevators = [
            int(i) for i in input().split()]
        for i in range(nb_elevators):
            # elevator_floor: floor on which this elevator is found
            # elevator_pos: position of the elevator on its floor
            elevator_floor, elevator_pos = [int(j) for j in input().split()]
            self.elevator_coors.setdefault(elevator_floor, []).append(elevator_pos)


class Act:
    clone = LeadClone()
    area = Area()
    wait_need = 0

    def needDirection(self):
        need_position = self.area.isExitHere(self.clone.clone_floor)
        if need_position != None:
            if (need_position < self.clone.clone_pos):
                return "LEFT"
            elif (need_position > self.clone.clone_pos):
                return "RIGHT"
        else:
            floor_coor = self.area.getClosest(self.clone.clone_floor, self.clone.clone_pos)
            print("Lift" + str(floor_coor), file=sys.stderr)
            if (floor_coor < self.clone.clone_pos):
                return "LEFT"
            elif (floor_coor > self.clone.clone_pos):
                return "RIGHT"
        return "STOP"

    def run(self):
        self.clone.getParams()

        if self.wait_need > 0:
            self.wait_need = self.wait_need - 1
            print("WAIT")
        else:
            need_dir = self.needDirection()
            print(need_dir, file=sys.stderr)
            if need_dir == "STOP":
                self.wait_need = 1
                print("WAIT")
            elif self.clone.direction in ['LEFT', 'RIGHT'] and self.clone.direction != need_dir:
                print("BLOCK")
                self.wait_need = 3
            else:
                print("WAIT")


act = Act()
while True:
    act.run()

