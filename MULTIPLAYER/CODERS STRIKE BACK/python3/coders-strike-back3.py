# https://www.codingame.com/ide/puzzle/coders-strike-back
# game loop
while True:
    # next_checkpoint_x: x position of the next check point
    # next_checkpoint_y: y position of the next check point
    # next_checkpoint_dist: distance to the next checkpoint
    # next_checkpoint_angle: angle between your pod orientation and the direction of the next checkpoint
    x, y, next_checkpoint_x, next_checkpoint_y, next_checkpoint_dist, next_checkpoint_angle = [int(i) for i in
                                                                                               input().split()]
    opponent_x, opponent_y = [int(i) for i in input().split()]
    trust = 0
    if next_checkpoint_angle > 90 or next_checkpoint_angle < -90:
        trust = str(10)
    else:
        if trust < 50:
            trust = 'BOOST'
        else:
            trust = str(100)

    # You have to output the target position
    # followed by the power (0 <= thrust <= 100)
    # i.e.: "x y thrust"
    print(str(next_checkpoint_x) + " " + str(next_checkpoint_y) + " " + trust)
# result https://www.codingame.com/replay/246125257