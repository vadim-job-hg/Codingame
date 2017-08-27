# game loop
while True:
    enemy_1 = raw_input()  # name of enemy 1
    dist_1 = int(raw_input())  # distance to enemy 1
    enemy_2 = raw_input()  # name of enemy 2
    dist_2 = int(raw_input())  # distance to enemy 2
    # Enter the code here
    if dist_1 < dist_2:
        print(enemy_1)
    else:
        print(enemy_2)