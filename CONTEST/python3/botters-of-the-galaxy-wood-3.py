import sys
import math


class BushAndSpawnPoint:
    def __init__(self, entity_type, x, y, radius):
        self.entity_type = entity_type
        self.x = int(x)
        self.y = int(y)
        self.radius = int(radius)


class Items:
    def __init__(self, item_name, item_cost, damage, health, max_health, mana, max_mana, move_speed, mana_regeneration,
                 is_potion):
        # item_name: contains keywords such as BRONZE, SILVER and BLADE, BOOTS connected by "_" to help you sort easier
        # item_cost: BRONZE items have lowest cost, the most expensive items are LEGENDARY
        # damage: keyword BLADE is present if the most important item stat is damage
        # move_speed: keyword BOOTS is present if the most important item stat is moveSpeed
        # is_potion: 0 if it's not instantly consumed
        self.item_name = item_name
        self.item_cost = int(item_cost)
        self.damage = int(damage)
        self.health = int(health)
        self.max_health = int(max_health)
        self.mana = int(mana)
        self.max_mana = int(max_mana)
        self.move_speed = int(move_speed)
        self.mana_regeneration = int(mana_regeneration)
        self.is_potion = int(is_potion)


class Unit:
    def __init__(self, unit_id, team, unit_type, x, y, attack_range, health, max_health, shield, attack_damage,
                 movement_speed, stun_duration, gold_value, count_down_1, count_down_2, count_down_3, mana, max_mana,
                 mana_regeneration, hero_type, is_visible, items_owned):
        # unit_type: UNIT, HERO, TOWER, can also be GROOT from wood1
        # shield: useful in bronze
        # stun_duration: useful in bronze
        # count_down_1: all countDown and mana variables are useful starting in bronze
        # hero_type: DEADPOOL, VALKYRIE, DOCTOR_STRANGE, HULK, IRONMAN
        # is_visible: 0 if it isn't
        # items_owned: useful from wood1

        self.unit_id = int(unit_id)
        self.team = int(team)
        self.unit_type = unit_type
        self.x = int(x)
        self.y = int(y)
        self.attack_range = int(attack_range)
        self.health = int(health)
        self.max_health = int(max_health)
        self.shield = int(shield)
        self.attack_damage = int(attack_damage)
        self.movement_speed = int(movement_speed)
        self.stun_duration = int(stun_duration)
        self.gold_value = int(gold_value)
        self.count_down_1 = int(count_down_1)
        self.count_down_2 = int(count_down_2)
        self.count_down_3 = int(count_down_3)
        self.mana = int(mana)
        self.max_mana = int(max_mana)
        self.mana_regeneration = int(mana_regeneration)
        self.is_visible = int(is_visible)
        self.items_owned = int(items_owned)

    def __str__(self):
        pass


class Hero(Unit):
    pass


class Tower(Unit):
    pass


class Game:
    def __init__(self):
        self.my_hero = None
        self.enemy_hero = None
        self.index = -1
        self.my_team = int(input())
        self.units = []
        bush_and_spawn_point_count = int(
            input())  # usefrul from wood1, represents the number of bushes and the number of places where neutral units can spawn
        self.bush_and_spawn_points = []
        for i in range(bush_and_spawn_point_count):
            # entity_type: BUSH, from wood1 it can also be SPAWN
            entity_type, x, y, radius = input().split()
            self.bush_and_spawn_points.append(BushAndSpawnPoint(entity_type, x, y, radius))

        item_count = int(input())  # useful from wood2
        self.items = []
        for i in range(item_count):
            item_name, item_cost, damage, health, max_health, mana, max_mana, move_speed, mana_regeneration, is_potion = input().split()
            self.items.append(
                Items(item_name, item_cost, damage, health, max_health, mana, max_mana, move_speed, mana_regeneration,
                      is_potion))

    def collect_data(self):
        self.index += 1
        self.gold = int(input())
        self.enemy_gold = int(input())
        self.round_type = int(input())  # a positive value will show the number of heroes that await a command
        entity_count = int(input())
        self.units.clear()
        self.my_hero = None
        self.enemy_hero = None
        for i in range(entity_count):
            unit_id, team, unit_type, x, y, attack_range, health, max_health, shield, attack_damage, movement_speed, stun_duration, gold_value, count_down_1, count_down_2, count_down_3, mana, max_mana, mana_regeneration, hero_type, is_visible, items_owned = input().split()
            if (unit_type == 'HERO'):
                if team == self.my_team:
                    self.my_hero = Hero(unit_id, team, unit_type, x, y, attack_range, health, max_health, shield,
                                        attack_damage, movement_speed, stun_duration, gold_value, count_down_1,
                                        count_down_2, count_down_3, mana, max_mana, mana_regeneration, hero_type,
                                        is_visible, items_owned)
                else:
                    self.enemy_hero = Hero(unit_id, team, unit_type, x, y, attack_range, health, max_health, shield,
                                           attack_damage, movement_speed, stun_duration, gold_value, count_down_1,
                                           count_down_2, count_down_3, mana, max_mana, mana_regeneration, hero_type,
                                           is_visible, items_owned)
            else:
                self.units.append(
                    Unit(unit_id, team, unit_type, x, y, attack_range, health, max_health, shield, attack_damage,
                         movement_speed, stun_duration, gold_value, count_down_1, count_down_2, count_down_3, mana,
                         max_mana, mana_regeneration, hero_type, is_visible, items_owned))

    def action(self):
        if self.index % 4 == 0 or self.index % 10 == 0:
            if (self.my_team == 0):
                print("MOVE 177.0 538.0")
            else:
                print("MOVE 1660.0 538.0")
        else:
            print("ATTACK_NEAREST UNIT")


game = Game()
print("IRONMAN")
# If roundType has a negative value then you need to output a Hero name, such as "DEADPOOL" or "VALKYRIE".
# Else you need to output roundType number of any valid action, such as "WAIT" or "ATTACK unitId"
# game loop
while True:
    game.collect_data()
    game.action()
    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)



