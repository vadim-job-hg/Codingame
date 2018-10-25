# https://github.com/texus/codingame/blob/master/Optimization/%20CodinGame%20Sponsored%20Contest.py
import sys

width = int(input())
height = int(input())
players = int(input())


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y


DIR = {'UP': 'C', 'RIGHT': 'A', 'DOWN': 'D', 'LEFT': 'E', 'STAY': 'B'}

grid = [['?' for x in range(width)] for y in range(height)]
enemies = [Player(-1, -1) for e in range(players - 1)]
player = Player(-1, -1)


def enemyAtPos(x, y):
    for e in enemies:
        if x == e.x and y == e.y:
            return True
    return False


def getPossibleMoves(x, y):
    possibleMoves = []
    if grid[(y - 1) % height][x] != '#':
        if not enemyAtPos(x, y - 1) and not enemyAtPos(x, y - 2) and not enemyAtPos(x - 1, y - 1) and not enemyAtPos(
                        x + 1, y - 1):
            possibleMoves.append([x, (y - 1) % height])
    if grid[y][(x + 1) % width] != '#':
        if not enemyAtPos(x + 1, y) and not enemyAtPos(x + 2, y) and not enemyAtPos(x + 1, y - 1) and not enemyAtPos(
                        x + 1, y + 1):
            possibleMoves.append([(x + 1) % width, y])
    if grid[(y + 1) % height][x] != '#':
        if not enemyAtPos(x, y + 1) and not enemyAtPos(x, y + 2) and not enemyAtPos(x - 1, y + 1) and not enemyAtPos(
                        x + 1, y + 1):
            possibleMoves.append([x, (y + 1) % height])
    if grid[y][(x - 1) % width] != '#':
        if not enemyAtPos(x - 1, y) and not enemyAtPos(x - 2, y) and not enemyAtPos(x - 1, y - 1) and not enemyAtPos(
                        x - 1, y + 1):
            possibleMoves.append([(x - 1) % width, y])

    return possibleMoves


def findNearestUnknown():  # BFS
    visited = []
    fringe = []  # our queue
    fringe.append(((player.x, player.y), []))

    while len(fringe) > 0:
        node = fringe.pop(0)  # node is a tuple of a location, and the path to that location
        if node[0] in visited:
            continue

        visited += [node[0]]

        if grid[node[0][1]][node[0][0]] == '?':
            return node[1][0]  # Return the location of the next step
        else:
            successors = getPossibleMoves(node[0][0], node[0][1])
            for successor in successors:
                path = node[1] + [(successor[0], successor[1])]
                fringe.append(((successor[0], successor[1]), path))

    return (player.x, player.y)


def findAlternativeMove():
    x, y = player.x, player.y

    # Move in any direction that makes us live at least one more turn
    if grid[(y - 1) % height][x] != '#' and not enemyAtPos(x, y - 1) and not enemyAtPos(x, y - 2) and not enemyAtPos(
                    x - 1, y - 1) and not enemyAtPos(x + 1, y - 1):
        return DIR['UP']
    if grid[y][(x + 1) % width] != '#' and not enemyAtPos(x + 1, y) and not enemyAtPos(x + 2, y) and not enemyAtPos(
                    x + 1, y - 1) and not enemyAtPos(x + 1, y + 1):
        return DIR['RIGHT']
    if grid[(y + 1) % height][x] != '#' and not enemyAtPos(x, y + 1) and not enemyAtPos(x, y + 2) and not enemyAtPos(
                    x - 1, y + 1) and not enemyAtPos(x + 1, y + 1):
        return DIR['DOWN']
    if grid[y][(x - 1) % width] != '#' and not enemyAtPos(x - 1, y) and not enemyAtPos(x - 2, y) and not enemyAtPos(
                    x - 1, y - 1) and not enemyAtPos(x - 1, y + 1):
        return DIR['LEFT']

    # We can't move, try to hit an enemy
    if enemyAtPos(x, y - 1):
        return DIR['UP']
    elif enemyAtPos(x + 1, y):
        return DIR['RIGHT']
    elif enemyAtPos(x, y + 1):
        return DIR['DOWN']
    elif enemyAtPos(x - 1, y):
        return DIR['LEFT']

    # There is no enemy next to us, just wait one turn
    return DIR['STAY']


# game loop
while True:
    up = input()
    right = input()
    down = input()
    left = input()

    for i in range(players):
        playerX, playerY = [int(j) for j in input().split()]
        if i + 1 == players:
            player.x, player.y = (playerX - 1) % width, (playerY - 1) % height
        else:
            enemies[i].x, enemies[i].y = (playerX - 1) % width, (playerY - 1) % height

    grid[player.y][player.x] = '_'
    grid[(player.y - 1) % height][player.x] = up
    grid[(player.y + 1) % height][player.x] = down
    grid[player.y][(player.x - 1) % width] = left
    grid[player.y][(player.x + 1) % width] = right

    # Debug information
    """
    for y in range(height):
        for x in range(width):
            if enemyAtPos(x, y):
                print('@', end='', file=sys.stderr)
            else:
                if x == player.x and y == player.y:
                    print('+', end='', file=sys.stderr)
                else:
                    print(grid[y][x], end='', file=sys.stderr)
        print(file=sys.stderr)
    """

    # Move towards unexplored areas
    x, y = findNearestUnknown()

    # Only make the suggested move when it doesn't get us killed
    if not enemyAtPos(x - 1, y) and not enemyAtPos(x + 1, y) and not enemyAtPos(x, y - 1) and not enemyAtPos(x, y + 1):
        if x == (player.x - 1) % width:
            print(DIR['LEFT'])
        elif y == (player.y - 1) % height:
            print(DIR['UP'])
        elif x == (player.x + 1) % width:
            print(DIR['RIGHT'])
        elif y == (player.y + 1) % height:
            print(DIR['DOWN'])
        else:
            print(DIR['STAY'])

    else:  # We need an alternative move (try keeping us alive as long as possible)
        print(findAlternativeMove())
