import sys
import math


# Made with love by AntiSquid, Illedan and Wildum.
# You can help children learn to code while you participate by donating to CoderDojo.
class Tactics:
    ATTACK = 'attack'
    DEFEND = 'defend'
    SUPPORT = 'support'
    TANK = 'tank'


class Point:
    def __init__(self, x, y, radius):
        self.x = int(x)
        self.y = int(y)
        self.radius = int(radius)

    def __hash__(self):
        return hash((self.x, self.y, self.radius))

    def __str__(self):
        return "{}x{}r{}".format(self.x, self.y, self.radius)

    def __repr__(self):
        return "Coors:<{}x{},r{}>".format(self.x, self.y, self.radius)


class SpawnPoint(Point):
    pass


class BushPoint(Point):
    pass


class Item:
    def __init__(self, item_name, item_cost, health):
        self.item_name = item_name
        self.item_cost = int(item_cost)
        self.health = int(health)
        '''
        max_health = int(max_health)
        mana = int(mana)
        max_mana = int(max_mana)
        move_speed = int(move_speed)
        mana_regeneration = int(mana_regeneration)
        is_potion = int(is_potion)
        '''

    def __hash__(self):
        return hash(self.item_name)


class ItemPotion(Item):
    def __init__(self, item_name, item_cost, health, max_health, mana, max_mana, move_speed, mana_regeneration):
        super().__init__(item_name, item_cost, health)
        print(self, health, file=sys.stderr)

        def __str__(self):
            return "ItemPotion item_name:{} item_cost:{} health:{}".format(self.item_name, self.item_cost, self.health)

            # def __repr__(self):
            #    return "Coors:<{}x{},r{}>".format(self.x, self.y, self.radius)

    class ItemUpgrade(Item):
        PRIORITY = {'Bronze': 1, 'Silver': 2, 'Golden': 3, 'Legendary': 4}

        def __init__(self, item_name, item_cost, damage, health, max_health, mana, max_mana, move_speed,
                     mana_regeneration):
            super().__init__(item_name, item_cost, health)
            # item_name: contains keywords such as BRONZE, SILVER and BLADE, BOOTS connected by "_" to help you sort easier
            for key, value in self.PRIORITY.items():
                if (item_name.find(key) != -1):
                    self._priority = key
                    break
            else:
                self._priority = 'OTHER'

            self.damage = int(damage)
            print(self, health, file=sys.stderr)

            def __str__(self):
                return "ItemUpgrade item_name:{} item_cost:{} damage:{} health:{}".format(self.item_name,
                                                                                          self.item_cost, self.damage,
                                                                                          self.health)

                # def __repr__(self):
                #    return "Coors:<{}x{},r{}>".format(self.x, self.y, self.radius)

        class Game:
            HEROES = ['DEADPOOL', 'DOCTOR_STRANGE', 'HULK', 'IRONMAN', 'VALKYRIE']
            tactics = {'DEADPOOL': Tactics.DEFEND, 'DOCTOR_STRANGE': Tactics.DEFEND, 'HULK': Tactics.DEFEND,
                       'IRONMAN': Tactics.DEFEND, 'VALKYRIE': Tactics.DEFEND}
            my_team = 0
            enemy_team = 1
            neitral_team = 2
            bushes_points = []
            spawn_points = []

            potion_items = []
            upgrade_items = []

            def __init__(self):
                self.my_team = int(input())
                self.enemy_team = [1, 0][self.my_team == 1]
                self._get_bush_and_spawn_point_count()
                self._get_items()

            def _append_point(self, entity_type, x, y, radius):
                # entity_type: BUSH, from wood1 it can also be SPAWN
                if (entity_type == 'BUSH'):
                    self.bushes_points.append(BushPoint(x, y, radius))
                elif (entity_type == 'SPAWN'):
                    self.spawn_points.append(SpawnPoint(x, y, radius))

            def _get_bush_and_spawn_point_count(self):
                bush_and_spawn_point_count = int(
                    input())  # useful from wood1, represents the number of bushes and the number of places where neutral units can spawn
                for i in range(bush_and_spawn_point_count):
                    entity_type, x, y, radius = input().split()
                    self._append_point(entity_type, x, y, radius)

            def _append_item(self, item_name, item_cost, damage, health, max_health, mana, max_mana, move_speed,
                             mana_regeneration, is_potion):
                # entity_type: BUSH, from wood1 it can also be SPAWN
                if (is_potion == '1'):
                    self.potion_items.append(
                        ItemPotion(item_name, item_cost, health, max_health, mana, max_mana, move_speed,
                                   mana_regeneration))
                else:
                    self.upgrade_items.append(
                        ItemUpgrade(item_name, item_cost, damage, health, max_health, mana, max_mana, move_speed,
                                    mana_regeneration))

            def _get_items(self):
                item_count = int(input())  # useful from wood2
                for i in range(item_count):
                    # item_cost: BRONZE items have lowest cost, the most expensive items are LEGENDARY
                    # damage: keyword BLADE is present if the most important item stat is damage
                    # move_speed: keyword BOOTS is present if the most important item stat is moveSpeed
                    # is_potion: 0 if it's not instantly consumed
                    item_name, item_cost, damage, health, max_health, mana, max_mana, move_speed, mana_regeneration, is_potion = input().split()
                    self._append_item(item_name, item_cost, damage, health, max_health, mana, max_mana, move_speed,
                                      mana_regeneration, is_potion)

        game = Game()

        print("HULK")
        print("IRONMAN")
        # game loop
        while True:
            gold = int(input())
            enemy_gold = int(input())
            round_type = int(input())  # a positive value will show the number of heroes that await a command
            entity_count = int(input())
            for i in range(entity_count):
                # unit_type: UNIT, HERO, TOWER, can also be GROOT from wood1
                # shield: useful in bronze
                # stun_duration: useful in bronze
                # count_down_1: all countDown and mana variables are useful starting in bronze
                # hero_type: DEADPOOL, VALKYRIE, DOCTOR_STRANGE, HULK, IRONMAN
                # is_visible: 0 if it isn't
                # items_owned: useful from wood1
                unit_id, team, unit_type, x, y, attack_range, health, max_health, shield, attack_damage, movement_speed, stun_duration, gold_value, count_down_1, count_down_2, count_down_3, mana, max_mana, mana_regeneration, hero_type, is_visible, items_owned = input().split()
                unit_id = int(unit_id)
                team = int(team)
                x = int(x)
                y = int(y)
                attack_range = int(attack_range)
                health = int(health)
                max_health = int(max_health)
                shield = int(shield)
                attack_damage = int(attack_damage)
                movement_speed = int(movement_speed)
                stun_duration = int(stun_duration)
                gold_value = int(gold_value)
                count_down_1 = int(count_down_1)
                count_down_2 = int(count_down_2)
                count_down_3 = int(count_down_3)
                mana = int(mana)
                max_mana = int(max_mana)
                mana_regeneration = int(mana_regeneration)
                is_visible = int(is_visible)
                items_owned = int(items_owned)

            # Write an action using print
            # To debug: print("Debug messages...", file=sys.stderr)


            # If roundType has a negative value then you need to output a Hero name, such as "DEADPOOL" or "VALKYRIE".
            # Else you need to output roundType number of any valid action, such as "WAIT" or "ATTACK unitId"
            print("ATTACK_NEAREST UNIT")
            print("ATTACK_NEAREST UNIT")