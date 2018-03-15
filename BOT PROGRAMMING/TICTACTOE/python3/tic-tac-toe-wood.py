import sys
import math


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
class Coors:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Grid:
    WINNING_COORS = [
        [Coors(0, 0), Coors(1, 0), Coors(2, 0)],
        [Coors(0, 1), Coors(1, 1), Coors(2, 1)],
        [Coors(0, 2), Coors(1, 2), Coors(2, 2)],
        [Coors(0, 0), Coors(0, 1), Coors(0, 2)],
        [Coors(1, 0), Coors(1, 1), Coors(1, 2)],
        [Coors(2, 0), Coors(2, 1), Coors(2, 2)],
        [Coors(0, 0), Coors(1, 1), Coors(2, 2)],
        [Coors(0, 2), Coors(1, 1), Coors(2, 0)],
    ]

    def __init__(self):
        self.m_grids = []  # my
        self.e_grids = []  # enemy


class TTT:
    def __init__(self):
        self.valid_actions = []
        self.grids = {(0, 0): Grid()}  # I know it ganna be more
        self._answer = Coors(1, 1)

    def get_data(self):
        opponent_row, opponent_col = [int(i) for i in input().split()]
        valid_action_count = int(input())
        self.valid_actions.clear()
        for i in range(valid_action_count):
            row, col = [int(j) for j in input().split()]
            self.valid_actions.append(Coors(row, col))

    def _set_oponent_action(self, opponent_row, opponent_col):
        if (opponent_row != -1 != opponent_col):
            self.grids[(0, 0)].e_grids.append(Coors(opponent_row, opponent_col))

    def action(self):
        self._find_best()
        self.answer()

    def _find_best(self):
        self._answer = Coors(self.valid_actions[0].x, self.valid_actions[0].y)

    def answer(self):
        self.grids[(0, 0)].m_grids.append(self._answer)
        print("{} {}".format(self._answer.x, self._answer.y))


# game loop
tic_tac_toe = TTT()
while True:
    tic_tac_toe.get_data()
    tic_tac_toe.action()
    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)