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
        print('ITEMS', item_name, item_cost, damage, health, max_health, mana, max_mana, move_speed, mana_regeneration,
              is_potion, file=sys.stderr)

class Unit:
    def __init__(self, unit_id, team, unit_type, x, y, attack_range, health, max_health, shield, attack_damage,
                 movement_speed, stun_duration, gold_value, count_down_1, count_down_2, count_down_3, mana,
                 max_mana, mana_regeneration, hero_type, is_visible, items_owned):
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
        # print(unit_id, team, unit_type, x, y, attack_range, health, max_health, shield, attack_damage, movement_speed, stun_duration, gold_value, count_down_1, count_down_2, count_down_3, mana, max_mana, mana_regeneration, hero_type, is_visible, items_owned, file=sys.stderr)

class Hero(Unit):
    pass

class Tower(Unit):
    pass

class Game:
    HEROES = []

    def __init__(self):
        self.byed_items = []
        self.my_hero = None
        self.enemy_hero = None
        self.index = -1
        self.my_team = int(input())
        self.my_units = []
        self.enemy_units = []
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
                Items(item_name, item_cost, damage, health, max_health, mana, max_mana, move_speed,
                      mana_regeneration, is_potion))

    def collect_data(self):
        self.index += 2
        self.gold = int(input())
        self.enemy_gold = int(input())
        self.round_type = int(input())  # a positive value will show the number of heroes that await a command
        entity_count = int(input())
        self.my_units.clear()
        self.enemy_units.clear()
        print('my team', self.my_team, file=sys.stderr)
        self.my_hero = None
        self.enemy_hero = None
        for i in range(entity_count):
            unit_id, team, unit_type, x, y, attack_range, health, max_health, shield, attack_damage, movement_speed, stun_duration, gold_value, count_down_1, count_down_2, count_down_3, mana, max_mana, mana_regeneration, hero_type, is_visible, items_owned = input().split()
            # print(unit_type,unit_type=='HERO', file=sys.stderr)
            if (unit_type == 'HERO'):
                if int(team) == self.my_team:
                    self.my_hero = Hero(unit_id, team, unit_type, x, y, attack_range, health, max_health,
                                        shield, attack_damage, movement_speed, stun_duration, gold_value,
                                        count_down_1, count_down_2, count_down_3, mana, max_mana,
                                        mana_regeneration, hero_type, is_visible, items_owned)
                else:
                    self.enemy_hero = Hero(unit_id, team, unit_type, x, y, attack_range, health, max_health,
                                           shield, attack_damage, movement_speed, stun_duration, gold_value,
                                           count_down_1, count_down_2, count_down_3, mana, max_mana,
                                           mana_regeneration, hero_type, is_visible, items_owned)
                    self.enemy_units.append(
                        Unit(unit_id, team, unit_type, x, y, attack_range, health, max_health, shield,
                             attack_damage, movement_speed, stun_duration, gold_value, count_down_1,
                             count_down_2, count_down_3, mana, max_mana, mana_regeneration, hero_type,
                             is_visible, items_owned))
            else:
                if int(team) == self.my_team:
                    self.my_units.append(
                        Unit(unit_id, team, unit_type, x, y, attack_range, health, max_health, shield,
                             attack_damage, movement_speed, stun_duration, gold_value, count_down_1,
                             count_down_2, count_down_3, mana, max_mana, mana_regeneration, hero_type,
                             is_visible, items_owned))
                else:
                    self.enemy_units.append(
                        Unit(unit_id, team, unit_type, x, y, attack_range, health, max_health, shield,
                             attack_damage, movement_speed, stun_duration, gold_value, count_down_1,
                             count_down_2, count_down_3, mana, max_mana, mana_regeneration, hero_type,
                             is_visible, items_owned))

        print('self.index', self.index, file=sys.stderr)

    def action(self):
        if (not (self.my_hero)):
            print("IRONMAN")
            return

        weakest = self.weakest_enemy_unit()
        closest = self.closest_enemy_unit()
        item_need_buy = self.get_best_item()
        need_health = self._need_health()
        if (need_health):
            self._buy(need_health)
            return

        if (item_need_buy):
            self.byed_items.append(item_need_buy)
            self._buy(item_need_buy)
            return

        if (self._go_back()):
            return

        enemy_avoid = self.need_avoid_damage()
        if (enemy_avoid):
            if (self.my_team == 0):
                self._move(self.my_hero.x - self.my_hero.attack_range + 10, enemy_avoid.y)
            else:
                self._move(self.my_hero.x + self.my_hero.attack_range - 10, enemy_avoid.y)
            return

        if (closest):
            self._attack(closest)
            return

        if weakest:
            self._attack(weakest)
            return

        print("ATTACK_NEAREST UNIT")

    # def _go_back_troops():

    def _go_back(self):
        if self.my_team == 0 and self.my_hero.x > 1300:
            self._move(1200, self.my_hero.y)
            return True
        elif self.my_team == 1 and self.my_hero.x < 500:
            self._move(600, self.my_hero.y)
            return True
        if self.my_team == 0:
            most_right = max(self.my_units, key=lambda x: x.x)
            if not (most_right):
                self._move(200, self.my_hero.y)
                return True
            elif most_right.x < self.my_hero.x:
                self._move(most_right.x - 5, self.my_hero.y)
                return True
        elif self.my_team == 1:
            most_left = min(self.my_units, key=lambda x: x.x)
            if not (most_left):
                self._move(1559, self.my_hero.y)
                return True
            elif most_left.x > self.my_hero.x:
                self._move(most_left.x + 5, self.my_hero.y)
                return True

        return False

    def _need_health(self):
        if not (self.my_hero) or self.my_hero.health > self.my_hero.max_health / 3:
            return None
        else:
            best_item = None
            for item in self.items:
                # print('OK', file=sys.stderr)
                if item.is_potion == 1 and self.gold > item.item_cost and (
                        best_item is None or best_item.health < item.health):
                    best_item = item
            # print(best_item.item_name, file=sys.stderr)
            return best_item

    def _buy(self, item):
        print("BUY {}".format(item.item_name))

    def _attack(self, unit):
        print("ATTACK {}".format(unit.unit_id))

    def _move(self, x, y):
        # print(x, y, file=sys.stderr)
        print("MOVE {} {}".format(x, y))

    def get_best_item(self):
        if not (self.my_hero):
            return None
        else:
            best_item = None
            for item in self.items:
                if (item.item_name.find('Bronze_') != -1 and self.index > 60):
                    continue
                if (item.item_name.find('Silver_') != -1 and self.index > 100):
                    continue
                if (item.item_name.find('Golden_') == -1 and self.index > 200):
                    continue
                # print('OK', file=sys.stderr)
                if item.is_potion == 0 and item.damage > 10 and self.gold > item.item_cost + 300 and (
                    not (best_item) or best_item.damage < item.damage):
                    best_item = item
            return best_item

    def weakest_enemy_unit(self):
        if len(self.enemy_units):
            return min(self.enemy_units, key=lambda x: x.health)

    def closest_enemy_unit(self):
        return None if not (self.my_hero) else min(self.enemy_units,
                                                   key=lambda x: x.health > 0 and abs(x.x - self.my_hero.x))

    def need_avoid_damage(self):
        # print(not(self.my_hero), self.my_hero, file=sys.stderr)
        if not (self.my_hero) or self.index > 100:
            return False
        # print((self.my_team==0 and self.my_hero.x<320) or (self.my_team==1 and self.my_hero.x>1540), file=sys.stderr)
        if ((self.my_team == 0 and self.my_hero.x < 320) or (self.my_team == 1 and self.my_hero.x > 1540)):
            return False

        for enemy in self.enemy_units:
            print(
            enemy.attack_range, self.my_hero.attack_range, abs(self.my_hero.x - enemy.x), file=sys.stderr)
            if enemy.unit_type == 'TOWER' and enemy.attack_range < self.my_hero.attack_range and abs(
                            self.my_hero.x - enemy.x) < enemy.attack_range:
                return enemy
        return False

game = Game()
# If roundType has a negative value then you need to output a Hero name, such as "DEADPOOL" or "VALKYRIE".
# Else you need to output roundType number of any valid action, such as "WAIT" or "ATTACK unitId"
# game loop
while True:
    game.collect_data()
    game.action()
    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)
