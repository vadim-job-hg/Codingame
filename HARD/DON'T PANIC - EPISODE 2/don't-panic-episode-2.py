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
        closest, pos = self.width, None
        print(closest, pos, self.elevator_coors, file=sys.stderr)
        for floor in self.elevator_coors.get(fl, []):
            print(floor, file=sys.stderr)
            if closest > abs(floor - cpos):
                closest = abs(floor - cpos)
                pos = floor
        return pos

    def __init__(self):
        self.nb_floors, self.width, self.nb_rounds, self.exit_floor, self.exit_pos, self.nb_total_clones, self.nb_additional_elevators, self.nb_elevators = [
            int(i) for i in input().split()]
        for i in range(self.nb_elevators):
            elevator_floor, elevator_pos = [int(j) for j in input().split()]
            self.elevator_coors.setdefault(elevator_floor, []).append(elevator_pos)
        print(self.elevator_coors, file=sys.stderr)
        self.build_best_path()




        # self.exit_floor


class Act:
    clone = LeadClone()
    area = Area()
    wait_need = 0

    def build_best_path(self):
        # nb_total_clones, nb_additional_elevators = self.nb_total_clones, self.nb_additional_elevators
        # first lets check no elevator levels

        # от  конца к началу строй
        for i in range(self.exit_floor, 0, -1):
            if self.elevator_coors.get(i, None) == None:
                self.each_floor_action[i] = 'ELEVATOR'
                self.nb_total_clones = self.nb_total_clones - 1
                self.nb_additional_elevators = self.nb_additional_elevators - 1
        another_floors = [x for x in range(self.exit_floor) if x not in self.each_floor_action.keys()]

    def calculate(self):

    def needDirection(self):
        if self.wait_need > 0:
            self.wait_need = self.wait_need - 1
            return "WAIT"
        else:
            action = self.area.each_floor_action.pop(self.clone.clone_floor, self.calculate())
            if action == 'BLOCK':
                self.wait_need = 2
            return action

    def run(self):
        self.clone.getParams()
        print(self.needDirection())


act = Act()
while True:
    act.run()
