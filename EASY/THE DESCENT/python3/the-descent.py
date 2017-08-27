# https://www.codingame.com/ide/puzzle/the-descent
# game loop
while True:
    mountain_max = 0
    index_max = 0
    for i in range(8):
        mountain_h = int(input())
        if mountain_max<mountain_h:
            mountain_max = mountain_h
            index_max = i
    print(str(index_max))

