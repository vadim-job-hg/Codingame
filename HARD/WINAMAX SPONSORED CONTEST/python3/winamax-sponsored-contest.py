import sys
import math
import string
from collections import deque

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

n = int(input())  # the number of cards for player 1

values_over10 = {'J': 11, 'Q': 12, 'K': 13, 'A': 14}


def get_value(card):
    if len(card) == 2:
        if card[0] in values_over10:
            value = values_over10[card[0]]
        else:
            value = int(card[0])
    elif len(card) == 3:
        value = int(card[0:2])
    return value


def winner(card1, card2):
    if get_value(card1) > get_value(card2):
        return 1
    elif get_value(card1) < get_value(card2):
        return 2
    else:
        return 0


def main():
    cardsP1 = deque([])
    cardsP2 = deque([])
    for i in xrange(n):
        cardp1 = input()  # the n cards of player 1
        cardsP1.append(cardp1)
    m = int(input())  # the number of cards for player 2
    for i in xrange(m):
        cardp2 = input()  # the m cards of player 2
        cardsP2.append(cardp2)

    card_roundP1 = deque([])
    card_roundP2 = deque([])

    rounds = 0
    while True:

        if len(cardsP2) == 0:
            print 1, rounds
            return
        if len(cardsP1) == 0:
            print 2, rounds
            return

        war = True
        while war == True:
            war = False
            card_roundP1.append(cardsP1.popleft())
            card_roundP2.append(cardsP2.popleft())

            P1 = card_roundP1[len(card_roundP1) - 1]
            P2 = card_roundP2[len(card_roundP2) - 1]
            winner_round = winner(P1, P2)
            print >> sys.stderr, P1, P2, winner_round
            if winner_round == 1:
                # print >> sys.stderr, card_roundP1
                for card in card_roundP1:
                    cardsP1.append(card)
                for card in card_roundP2:
                    cardsP1.append(card)
                card_roundP1.clear()
                card_roundP2.clear()

            elif winner_round == 2:
                for card in card_roundP1:
                    cardsP2.append(card)
                for card in card_roundP2:
                    cardsP2.append(card)
                card_roundP1.clear()
                card_roundP2.clear()
            elif winner_round == 0:
                if len(cardsP1) < 4 or len(cardsP2) < 4:
                    print "PAT"
                    return
                for i in range(3):
                    card_roundP1.append(cardsP1.popleft())
                    card_roundP2.append(cardsP2.popleft())
                war = True
        # print >> sys.stderr, len(cardsP1)
        rounds += 1

        # Write an action using print
        # To debug: print >> sys.stderr, "Debug messages..."


if __name__ == "__main__":
    main()