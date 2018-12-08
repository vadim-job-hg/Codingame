import sys
import math
import random


# 5 low costers
# 5 guard
# 5 Breakthrough
# 5 Charge
# + Priority creaters list

class ValidActions:
    PICK = 'PICK {}'
    PASS = 'PASS'
    SUMMON = 'SUMMON {}'
    ATTACK = 'ATTACK {} {}'


class Action:
    def __init__(self, action=ValidActions.PASS, params=[]):
        self.set_data(action, params)

    def set_data(self, action=ValidActions.PASS, params=[]):
        self.action = action
        self.params = params

    def __str__(self):
        print(self.action, self.params, file=sys.stderr)
        return self.action.format(*self.params)


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
        self.abilities = abilities
        print(self.abilities, file=sys.stderr)
        self.my_health_change = int(my_health_change)
        self.opponent_health_change = int(opponent_health_change)
        self.card_draw = int(card_draw)

    def __str__(self):
        return '{}'.format(self.card_number)

    def __hash__(self):
        return self.instance_id

    def is_guard(self):
        return self.abilities[3] == 'G'

    def is_break(self):
        return self.abilities[0] == 'B'

    def is_charge(self):
        return self.abilities[1] == 'C'

    def get_points(self):
        point = 0
        if (self.is_guard()):
            point += 40 * self.defense

        if (self.is_break()):
            point += 3 * self.attack

        if (self.is_charge()):
            point += 3 * self.attack

        # if more than one ability

        point += math.pow(2, 13 - self.cost) / 50
        point += self.attack * 3
        point += self.defense
        return point


class Collection():
    def __init__(self):
        self._carts = []

    def add(self, cart: Cart) -> None:
        self._carts.append(cart)

    def remove(self, cart: Cart) -> None:
        for u in self._carts:
            if u == cart:
                self._carts.remove(u)
                break


class Game:
    def __init__(self):
        self.turn = 0
        self.phase = 'DRAFT'
        self.actions = []
        self.cards = []
        self.my_board = []
        self.en_board = []
        self.my_hand = []

    def run(self):
        while True:
            self.clear_data()
            self.upd_data()
            if (self.phase == 'DRAFT'):
                self.draft()
            else:
                self.battle()
            self.print_actions()

    def clear_data(self):
        self.actions.clear()
        self.cards.clear()
        self.my_board.clear()
        self.en_board.clear()
        self.my_hand.clear()
        self.summoned_count = 0

    def upd_data(self):
        self.turn += 1
        # for i in range(2):
        self.player_health, self.player_mana, self.player_deck, self.player_rune, self.player_draw = [int(j) for j in
                                                                                                      input().split()]
        self.eplayer_health, self.eplayer_mana, self.eplayer_deck, self.eplayer_rune, self.eplayer_draw = [int(j) for j
                                                                                                           in
                                                                                                           input().split()]

        self.opponent_hand, self.opponent_actions = [int(i) for i in input().split()]
        for i in range(self.opponent_actions):
            card_number_and_action = input()

        self.card_count, self.carts = int(input()), []
        for i in range(self.card_count):
            data = input().split()
            self.carts.append(Cart(*data))

    def draft(self):

        points_cur, number_cur, index = 0, 0, 0
        for cart in self.carts:
            if (points_cur < cart.get_points()):
                points_cur = cart.get_points()
                number_cur = index
            index += 1
        # self.my_carts.append(carts[0])
        self.actions.append(Action(ValidActions.PICK, [number_cur]))
        if (self.turn >= 30):
            self.phase = 'BATTLE'

    def get_board(self):
        for cart in self.carts:
            if (cart.location == -1):
                self.en_board.append(cart)
            elif (cart.location == 1):
                self.summoned_count += 1
                self.my_board.append(cart)
            else:
                self.my_hand.append(cart)

    def summon(self):
        if (len(self.my_board) < self.summon_optimal_count):
            current_cart, points_cur = None, 0
            for cart in self.my_hand:
                if (points_cur < cart.get_points() and self.player_mana >= cart.cost):
                    points_cur = cart.get_points()
                    current_cart = cart

            if (current_cart):
                self.actions.append(Action(ValidActions.SUMMON, [current_cart.instance_id]))
                self.player_mana -= cart.cost
                if (current_cart.is_charge()):
                    self.attack_best(current_cart)

    def attack(self):
        print(sorted(self.my_board, key=lambda cart: cart.is_guard()), file=sys.stderr)
        for cart in sorted(self.my_board, key=lambda cart: cart.is_guard()):
            if (self.player_mana <= cart.cost):
                self.attack_best(cart)
                self.player_mana -= cart.cost

    def attack_best(self, who):
        target = -1
        if (any(cart.is_guard() for cart in self.en_board)):
            current_cart, points_cur = None, 0
            for cart in self.en_board:
                if (points_cur < cart.get_points() and cart.is_guard() and cart.defense > 0):
                    points_cur = cart.get_points()
                    current_cart = cart

            if (current_cart):
                target = current_cart.instance_id
                current_cart.defense -= who.attack

        if (target == -1 and random.randint(0, 1) != 0):
            current_cart, points_cur = None, 0
            for cart in self.en_board:
                if (points_cur < cart.get_points() and cart.defense > 0):
                    points_cur = cart.get_points()
                    current_cart = cart

            if (current_cart):
                target = current_cart.instance_id
                current_cart.defense -= who.attack

        self.actions.append(Action(ValidActions.ATTACK, [who.instance_id, target]))

    def battle(self):
        self.get_board()
        self.summon_optimal_count = math.ceil(self.player_mana / 2)
        if (self.summon_optimal_count > 6):
            self.summon_optimal_count = 6
        if (self.summon_optimal_count < 2):
            self.summon_optimal_count = 2
        # self.summon_optimal_count = 3
        self.summon()
        self.attack()

        '''
        act, mana, summoned = [], 0, False
        for cart in my_carts:
            if(mana+cart.cost<=self.player_mana):
                if(cart.location==0):
                    if(not(summoned) and self.summoned_count<6):
                        self.actions.append(Action(ValidActions.SUMMON, [cart.instance_id]))                    
                        summoned = True
                        mana += cart.cost
                else:
                    target = -1
                    self.actions.append(Action(ValidActions.ATTACK, [cart.instance_id, target]))
                    mana += cart.cost
        '''

    def print_actions(self):
        if (len(self.actions)):
            act = []
            for action in self.actions:
                act.append(str(action))
            print(';'.join(act))
        else:
            print('PASS')


game = Game()
game.run()

