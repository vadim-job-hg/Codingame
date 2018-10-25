# https://www.codingame.com/ide/puzzle/the-last-crusade-episode-1
MAP_RULES = {
    '0':{},
    '1':{'LEFT':'BOTTOM', 'TOP':'BOTTOM', 'RIGHT':'BOTTOM'},
    '2':{'LEFT':'RIGHT', 'RIGHT':'LEFT'},
    '3':{'TOP': 'BOTTOM'},
    '4':{'TOP':'LEFT', 'RIGHT': 'BOTTOM'},
    '5':{'TOP':'RIGHT', 'LEFT': 'BOTTOM'},
    '6':{'LEFT':'RIGHT', 'RIGHT':'LEFT'},
    '7':{'TOP':'BOTTOM', 'RIGHT':'BOTTOM'},
    '8':{'LEFT':'BOTTOM', 'RIGHT':'BOTTOM'},
    '9':{'LEFT':'BOTTOM', 'TOP': 'BOTTOM'},
    '10':{'TOP':'LEFT'},
    '11':{'TOP':'RIGHT'},
    '12':{'RIGHT':'BOTTOM'},
    '13':{'LEFT':'BOTTOM'},
}
DIR_RULES = {
    'LEFT':{'y':0,'x':-1},
    'RIGHT':{'y': 0, 'x':1},
    'BOTTOM':{'y': 1, 'x':0}
}
# w: number of columns.
# h: number of rows.
w, h = [int(i) for i in input().split()]
map = []
for i in range(h):
    # represents a line in the grid and contains W integers. Each integer represents one room of a given type.
    map.append(input().split())
ex = int(input())  # the coordinate along the X axis of the exit (not useful for this first mission, but must be read).

# game loop
while True:
    xi, yi, pos = input().split()
    xi = int(xi)
    yi = int(yi)
    rule = DIR_RULES[MAP_RULES[map[yi][xi]][pos]]
    x_to, y_to = xi+rule['x'], yi+rule['y']
    # One line containing the X Y coordinates of the room in which you believe Indy will be on the next turn.
    print("{0} {1}".format(x_to, y_to))
