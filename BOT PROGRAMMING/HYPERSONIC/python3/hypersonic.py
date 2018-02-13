# https://github.com/waniz/katas_hackerrank_codingame_codewars/blob/master/codingame/contests/hypersonic/hypersonic.py
# https://www.codingame.com/ide/puzzle/hypersonic
import sys
import math

# To debug: print("Debug messages...", file=sys.stderr)
# constants
BOMB_DECIDE_LIMIT = 1


class Emulator:
    def find_spot_for_bomb(self, matrix):
        self.matrix = matrix

        # 2 bombs criteria
        for matrix_row in range(1, height - 2):
            for position_in_row in range(1, width - 2):
                bomb_ev = 0
                if matrix[matrix_row][position_in_row - 1] == '0':
                    bomb_ev += 1
                if matrix[matrix_row][position_in_row + 1] == '0':
                    bomb_ev += 1
                if matrix[matrix_row - 1][position_in_row] == '0':
                    bomb_ev += 1
                if matrix[matrix_row + 1][position_in_row] == '0':
                    bomb_ev += 1

                if bomb_ev >= BOMB_DECIDE_LIMIT + 1:
                    # print(bomb_ev, file=sys.stderr)
                    # print(matrix_column, matrix_row, file=sys.stderr)
                    return position_in_row, matrix_row

        # 1 bombs criteria
        for matrix_row in range(1, height - 2):
            for position_in_row in range(1, width - 2):
                if matrix[matrix_row][position_in_row] == '0':
                    return position_in_row, matrix_row
        return 1, 1


class InputData:
    def fill_player_data(self, type, owner, x, y, p_1, p_2):
        pass


class BomberMan:
    def my_position(self, position_x, position_y):
        self.x = position_x
        self.y = position_y


bomberman = BomberMan()
turn_data = InputData()
emulator = Emulator()

width, height, my_id = [int(i) for i in input().split()]  # 13 columns x 11 rows
# print(width, height, my_id, file=sys.stderr)
while True:

    # field structure: row, position // row = y, position x, structure = field[y, x]
    field = []
    for i in range(height):
        row = input()
        field.append(row)

    # entities frame:
    # entity_type: 0 - player, 1 - bomb, 2 - item
    # owner      : for player - ID player (0, 1), for bomb - ID player's, item - ignored (always 0)
    # position   : x, y
    # param_1    : for player - number of bomb possible, for bomb - number until boom, item - int representing item
    # param_2    : for player - current explosive range of bomb, for bomb - current explosive range, item - ignored (0)
    entities = int(input())
    for i in range(entities):
        entity_type, owner, x, y, param_1, param_2 = [int(j) for j in input().split()]
        if my_id == owner:
            bomberman.x = x
            bomberman.y = y

    # core part
    bomb_x, bomb_y = emulator.find_spot_for_bomb(field)

    if bomb_x == bomberman.x and bomb_y == bomberman.y:
        print('BOMB %s %s' % (bomb_x, bomb_y))
    else:
        print('MOVE %s %s' % (bomb_x, bomb_y))

