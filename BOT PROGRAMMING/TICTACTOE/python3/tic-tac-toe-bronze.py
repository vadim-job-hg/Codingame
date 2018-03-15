import sys
import math
# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
class Coors:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.local = self if x < 3 and y < 3 else Coors(x % 3, y % 3)

    def base_coors(self):
        return (int(self.x / 3), int(self.y / 3))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return "{}x{}".format(self.x, self.y)

    def __repr__(self):
        return "Coors:<{}x{}>".format(self.x, self.y)


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
    PRIORITY = {
        (1, 1): 3,
        (0, 2): 2,
        (2, 2): 2,
        (2, 0): 2,
        (0, 0): 2,
        # other 1
    }

    def __init__(self, bx=0, by=0):
        self.m_grids = []  # my
        self.e_grids = []  # enemy
        self.bx, self.by = bx, by
        self.m_priority_to_finish = {}
        self.e_priority_to_finish = {}

    def _refresh(self, valid_actions):
        print('self.m_grids', self.m_grids, file=sys.stderr)
        self.m_priority_to_finish.clear()
        for action in valid_actions:
            self.m_priority_to_finish[(action.x, action.y)] = 0
            for winning in self.WINNING_COORS:
                cur_value = 0
                if action.local in winning:
                    cur_value = 1
                    # print('{} in {}'.format(action.local, winning), file=sys.stderr)

                for my in self.m_grids:
                    if my.local in winning:
                        print('{} in {}'.format(my.local, winning), file=sys.stderr)
                        cur_value += 1

                if (self.m_priority_to_finish.get((action.x, action.y), 0) < cur_value):
                    self.m_priority_to_finish[(action.x, action.y)] = cur_value

        print('self.m_priority_to_finish', self.m_priority_to_finish, file=sys.stderr)
        # self.m_priority_to_finish

    def best_coor(self, valid_actions):
        this_grid_actions = self.filter_for_this_grid(valid_actions)
        self._refresh(this_grid_actions)
        this_grid_actions = self.filter_priority_to_finish(this_grid_actions)
        print(self.m_grids, file=sys.stderr)
        priority = self.priority_filter(this_grid_actions)
        return priority.pop()

    def filter_priority_to_finish(self, actions):
        max_priority = self.max_priority_to_finish(actions)
        return set(x for x in actions if self.m_priority_to_finish.get((x.x, x.y), 0) == max_priority)

    def max_priority_to_finish(self, actions):
        return max(self.m_priority_to_finish.get((x.x, x.y), 0) for x in actions)

    def filter_for_this_grid(self, actions):
        return set(x for x in actions if self.bx == int(x.x / 3) and self.by == int(x.y / 3))

    def priority_filter(self, actions):
        max_priority = self.max_priority(actions)
        return set(x for x in actions if self.PRIORITY.get((x.x % 3, x.y % 3), 1) == max_priority)

    def max_priority(self, actions):
        return max(self.PRIORITY.get((x.x % 3, x.y % 3), 1) for x in actions)

class TTT:
    def __init__(self):
        self.valid_actions = set()
        self.valid_base = set()
        self.grids = {
            (0, 0): Grid(0, 0), (0, 1): Grid(0, 1), (0, 2): Grid(0, 2),
            (1, 0): Grid(1, 0), (1, 1): Grid(1, 1), (1, 2): Grid(1, 2),
            (2, 0): Grid(2, 0), (2, 1): Grid(2, 1), (2, 2): Grid(2, 2),
            'base': Grid()
        }
        self._answer = Coors(1, 1)

    def get_data(self):
        opponent_row, opponent_col = [int(i) for i in input().split()]
        self._save_enemy_answer(Coors(opponent_row, opponent_col))
        valid_action_count = int(input())
        self.valid_actions.clear()
        self.valid_base.clear()
        for i in range(valid_action_count):
            row, col = [int(j) for j in input().split()]
            # print(row, col, file=sys.stderr)
            self.valid_actions.add(Coors(row, col))
            self.valid_base.add(Coors(int(row / 3), int(col / 3)))
            # print(row, col, file=sys.stderr)

    def action(self):
        self._find_best()
        self.answer()

    def _find_best(self):
        base_best = self.grids['base'].best_coor(self.valid_base)
        # print('base_best', base_best, file=sys.stderr)
        best_in_grid = self.grids[(base_best.x, base_best.y)].best_coor(self.valid_actions)
        print('best_in_grid', best_in_grid, file=sys.stderr)
        self._answer = Coors(best_in_grid.x, best_in_grid.y)

    def answer(self):
        self._save_my_answer()
        print("{} {}".format(self._answer.x, self._answer.y))

    def _save_my_answer(self):
        self.grids[self._answer.base_coors()].m_grids.append(self._answer.local)

    def _save_enemy_answer(self, enemy_answer):
        if (enemy_answer.x != -1 and enemy_answer.y != -1):
            self.grids[enemy_answer.base_coors()].e_grids.append(enemy_answer.local)

# game loop
tic_tac_toe = TTT()
while True:
    tic_tac_toe.get_data()
    tic_tac_toe.action()
    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)