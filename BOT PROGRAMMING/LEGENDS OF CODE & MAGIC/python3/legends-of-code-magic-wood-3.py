import sys
import math
import random


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
class Cart:
    def __init__(self, card_number, instance_id, location, card_type, cost, attack, defense, abilities,
                 my_health_change, opponent_health_change, card_draw):
        self.card_number = int(card_number)
        self.instance_id = int(instance_id)
        self.location = int(location)
        self.card_type = int(card_type)
        self.cost = int(cost)
        self.attack = int(attack)
        self.defense = int(defense)
        self.my_health_change = int(my_health_change)
        self.opponent_health_change = int(opponent_health_change)
        self.card_draw = int(card_draw)

    def __str__(self):
        return '{}'.format(self.card_number)


class Game:
    def __init__(self):
        self.turn = 0
        self.phase = 'DRAFT'
        self.my_carts = []

    def run(self):
        while True:
            self.upd_data()
            print(self.phase, file=sys.stderr)
            if (self.phase == 'DRAFT'):
                self.draft()
            else:
                self.battle()

    def upd_data(self):
        self.turn += 1
        for i in range(2):
            player_health, player_mana, player_deck, player_rune, player_draw = [int(j) for j in input().split()]

        opponent_hand, opponent_actions = [int(i) for i in input().split()]
        for i in range(opponent_actions):
            card_number_and_action = input()

    def draft(self):
        card_count, carts = int(input()), []
        for i in range(card_count):
            data = input().split()
            carts.append(Cart(*data))

        print(carts, file=sys.stderr)
        # Write an action using print
        # To debug: print("Debug messages...", file=sys.stderr)

        print('PICK {}'.format(random.randint(0, 2)))
        self.my_carts.append(carts[0])
        if (len(self.my_carts) >= 30):
            self.phase = 'BATTLE'

    def battle(self):
        card_count, carts = int(input()), []
        for i in range(card_count):
            data = input().split()
            carts.append(Cart(*data))

        print('PASS')


game = Game()
game.run()

