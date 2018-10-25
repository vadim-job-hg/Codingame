import sys
import math

DEBUG = True


def debug(*args):
    if (DEBUG):
        print(args,
              file=sys.stderr)  # Bring data on patient samples from the diagnosis machine to the laboratory with enough molecules to produce medicine!

MAP = [16000, 7500]
WIZARD_RADIUS = 400
SNAFFLE_RADIUS = 150
MY_TEAM_ID = int(input())  # if 0 you need to score on the right of the map, if 1 you need to score on the left

if MY_TEAM_ID == 0:
    GOALS = [16000, 3750]
else:
    GOALS = [0, 3750]

class Entities:
    entities_id = None
    entity_type = None  # "WIZARD", "OPPONENT_WIZARD" or "SNAFFLE" (or "BLUDGER" after first league)
    x = None
    y = None
    vx = None
    vy = None
    state = None  # 1 - wizard grabbed snaffle, 0 - otherwise

    def __init__(self, data):
        self.entities_id = data[0]
        self.entity_type = data[1]
        self.x = data[2]
        self.y = data[3]
        self.vx = data[4]
        self.vy = data[5]
        self.state = data[6]

class Player:
    x = None
    y = None
    vx = None
    vy = None
    state = None

    def __init__(self, data):
        self.entities_id = data.entities_id
        self.entity_type = data.entity_type
        self.x = data.x
        self.y = data.y
        self.vx = data.vx
        self.vy = data.vy
        self.state = data.state

    def get_distance_to(self, target):
        return math.hypot(abs(self.x - target.x), abs(self.y - target.y))

    def get_snaffle(self, all_entities):
        min_dist_to_snaffle = float('inf')
        snaffle = None
        for target in all_entities:
            if target.entity_type != 'SNAFFLE':
                continue
            if self.get_distance_to(target) <= min_dist_to_snaffle:
                min_dist_to_snaffle = self.get_distance_to(target)
                snaffle = target
        return snaffle

    @staticmethod
    def move(x, y, thruster):
        print('MOVE %s %s %s' % (x, y, thruster))

    @staticmethod
    def throw(x, y, power):
        print('THROW %s %s %s' % (x, y, power))

# print(game_entities, file=sys.stderr)
# game loop
while True:
    game_entities = []
    myScore, myMagic = input().split()
    opponentScore, opponentMagic = input().split()
    entities = int(input())  # number of entities still in game
    for _ in range(entities):
        entity_id, entity_type, x, y, vx, vy, state = input().split()
        entitie = Entities([int(entity_id), entity_type, int(x), int(y), int(vx), int(vy), int(state)])
        game_entities.append(entitie)

    player_num = 1
    my_wizard_1, my_wizard_2 = None, None
    for entitie in game_entities:
        if entitie.entity_type == 'WIZARD':
            if player_num == 1:
                player_num += 1
                my_wizard_1 = Player(entitie)
            elif player_num == 2:
                my_wizard_2 = Player(entitie)

    target_1 = my_wizard_1.get_snaffle(all_entities=game_entities)
    target_2 = my_wizard_2.get_snaffle(all_entities=game_entities)

    if my_wizard_1.get_distance_to(target_1) > WIZARD_RADIUS:
        my_wizard_1.move(target_1.x, target_1.y, thruster=150)
    else:
        my_wizard_1.throw(GOALS[0], GOALS[1], power=500)

    if my_wizard_2.get_distance_to(target_2) > WIZARD_RADIUS:
        my_wizard_2.move(target_2.x, target_2.y, thruster=150)
    else:
        my_wizard_2.throw(GOALS[0], GOALS[1], power=500)