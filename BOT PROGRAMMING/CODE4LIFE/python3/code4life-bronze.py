import sys
import math
import operator
import random

DEBUG = True


def debug(*args):
    if (DEBUG):
        print(args,file=sys.stderr)  # Bring data on patient samples from the diagnosis machine to the laboratory with enough molecules to produce medicine!

class Plans:
    COLLECT_MOLECULES = 'COLLECT_MOLECULES'  # just grab 10 molecules
    COLLECT_SAMPLES_MOLECULES = 'COLLECT_SAMPLES_MOLECULES'  # grab for samples
    COLLECT_SAMPLES = 'COLLECT_SAMPLES'
    DIAGNOSE_SAMPLES = 'DIAGNOSE_SAMPLES'
    CHECK_SAMPLES = 'CHECK_SAMPLES'
    FINISH_SAMPLE = 'FINISH_SAMPLE'

class Molecules:
    MOLECULES = ['A', 'B', 'C', 'D', 'E']

    def __init__(self, data=None):
        if data is None:
            self.data = {key: 0 for key in self.MOLECULES}
        else:
            self.put_data(data)

    def put_data(self, data):
        self.data = dict(zip(self.MOLECULES, [int(j) for j in data]))

    def get_count(self):
        return sum(self.data.values())

    def get_min_key(self):
        return min(self.data.items(), key=lambda x: x[0])

    def __str__(self):
        return str(self.data)

class Project:
    def __init__(self, data):
        self.data = Molecules(data.split())

class Robot:
    def __init__(self):
        self.storage_molecules = Molecules()
        self.expertise_molecules = Molecules()

    def put_data(self, data):
        self.target, eta, score, storage_a, storage_b, storage_c, storage_d, storage_e, expertise_a, expertise_b, expertise_c, expertise_d, expertise_e = data
        self.eta = int(eta)
        self.score = int(score)
        self.storage_molecules.put_data([storage_a, storage_b, storage_c, storage_d, storage_e])
        self.expertise_molecules.put_data([expertise_a, expertise_b, expertise_c, expertise_d, expertise_e])

class Player(Robot):
    plan = Plans.COLLECT_SAMPLES
    target_sample = None
    moving = 0
    samples = {}
    finished = []
    care_samples = 3
    max_rank = 1

    def can_finish(self, sample):
        for key, value in sample.molecules_cost.data.items():
            if value > self.storage_molecules.data[key] + self.expertise_molecules.data[key]:
                return False
        else:
            return True

    def isMoving(self):
        self.moving -= 1
        return self.moving > 0

    def put_data(self, data):
        super().put_data(data)

    def molecules_count(self):
        return self.storage_molecules.get_count()

    def need_more(self, key, value):
        if value > 0:
            debug('need_more', key, value)
            debug('storage_molecules', self.storage_molecules.data[key])
            debug('self.expertise_molecules', self.expertise_molecules.data[key])
            debug('return ', value > self.storage_molecules.data[key] + self.expertise_molecules.data[key])
        if value > self.storage_molecules.data[key] + self.expertise_molecules.data[key]:
            return True
        else:
            return False

class Sample:
    def __init__(self, data):
        sample_id, carried_by, rank, self.expertise_gain, health, cost_a, cost_b, cost_c, cost_d, cost_e = data.split()
        self.sample_id = int(sample_id)
        self.carried_by = int(carried_by)
        self.rank = int(rank)
        self.health = int(health)
        self.molecules_cost = Molecules([cost_a, cost_b, cost_c, cost_d, cost_e])

    def __str__(self):
        return self.sample_id + ': ' + str(self.molecules_cost)

class Game:
    _round = 0
    projects = []
    players_count = 2
    my_player_id = 0
    molecules = Molecules()
    players = []
    sample_count = 0
    samples = []
    MOVING_TABLE = {
        ('START_POS', 'DIAGNOSIS'): 2, ('START_POS', 'MOLECULES'): 2,
        ('START_POS', 'LABORATORY'): 2, ('START_POS', 'SAMPLES'): 2,
        ('SAMPLES', 'DIAGNOSIS'): 3, ('DIAGNOSIS', 'SAMPLES'): 3,
        ('SAMPLES', 'MOLECULES'): 3, ('MOLECULES', 'SAMPLES'): 3,
        ('SAMPLES', 'LABORATORY'): 3, ('LABORATORY', 'SAMPLES'): 3,
        ('MOLECULES', 'DIAGNOSIS'): 3, ('DIAGNOSIS', 'MOLECULES'): 3,
        ('MOLECULES', 'LABORATORY'): 3, ('LABORATORY', 'MOLECULES'): 3,
        ('LABORATORY', 'DIAGNOSIS'): 4, ('DIAGNOSIS', 'LABORATORY'): 4
    }

    def __init__(self):
        self.project_count = int(input())
        for i in range(self.project_count):
            self.projects.append(Project(input()))
        self.current_player = Player()
        for i in range(1, self.players_count):
            self.players.append(Robot())

    def run(self):
        self._round += 1
        self._collect_data()
        debug('<============COLLECTED DATA============>')
        self._debug()
        self._action()

    def _collect_data(self):
        self.current_player.put_data(input().split())
        for i in range(self.players_count - 1):
            self.players[i].put_data(input().split())
        self.molecules.put_data(input().split())
        self.sample_count = int(input())
        self.samples.clear()
        for i in range(self.sample_count):
            self.samples.append(Sample(input()))
        self.current_player.samples = self._get_player_samples_dict(self.my_player_id)

    def _get_player_samples(self, player_id):
        return [x for x in self.samples if x.carried_by == player_id]  # -self.current_player.finished

    def _get_player_samples_dict(self, player_id):
        return {x.sample_id: x for x in self.samples if x.carried_by == player_id}

    def _get_player_samples_dict_data(self, player_id):
        return {x.sample_id: x.molecules_cost.data for x in self.samples if x.carried_by == player_id}

    def _debug(self):
        debug('ROUND #{}'.format(self._round), 'PLAN =>{}'.format(self.current_player.plan),
              'Target position [{}]'.format(self.current_player.target))
        debug('Carry molecules ', self.current_player.storage_molecules.data)
        debug('Expertise molecules ', self.current_player.expertise_molecules.data)
        debug('User Samples ', str(self._get_player_samples_dict_data(self.my_player_id)))
        debug('Nobody Samples ', self._get_player_samples_dict_data(-1))

    def _action(self):
        # todo: check if can finish right now
        if self.current_player.isMoving():
            print("WAIT")
            return

        if self.current_player.plan == Plans.COLLECT_MOLECULES:
            self._collect_molecules()
        elif self.current_player.plan == Plans.COLLECT_SAMPLES:
            self._collect_samples()
        elif self.current_player.plan == Plans.DIAGNOSE_SAMPLES:
            self._diagnose_samples()
        elif self.current_player.plan == Plans.CHECK_SAMPLES:
            self._check_samples()
        elif self.current_player.plan == Plans.COLLECT_SAMPLES_MOLECULES:
            self._collect_sample_molecules()
        elif self.current_player.plan == Plans.FINISH_SAMPLE:
            self._finish_samples()
        else:
            print("WAIT")

    def _collect_molecules(self):
        if self.current_player.molecules_count() < 5 and self.molecules.get_count() > 0:
            if self.current_player.target != 'MOLECULES':
                self._move('MOLECULES')
            else:
                key = random.choice(Molecules.MOLECULES)
                if (self.molecules.data[key] > 0):
                    print("CONNECT {}".format(key))
                    return
                storage_molecules = sorted(self.current_player.storage_molecules.data.items(),
                                           key=lambda x: x[1], reverse=True)
                for key in storage_molecules:
                    if self.molecules.data[key[0]] > 0:
                        print("CONNECT {}".format(key[0]))
                        return
        else:
            self.current_player.plan = Plans.COLLECT_SAMPLES
            debug('******************change plan({})**********************'.format(self.current_player.plan))
            self._action()

    def _collect_samples(self):
        if len(self.current_player.samples) < self.current_player.care_samples:
            if self.current_player.target != 'SAMPLES':
                self._move('SAMPLES')
            else:
                if (len(self.current_player.finished) < 3):
                    print("CONNECT {}".format(random.choice([1, 1, 1, 2])))
                elif (len(self.current_player.finished) < 6):
                    print("CONNECT {}".format(random.choice([1, 2, 2, 2, 2, 2, 2])))
                elif (len(self.current_player.finished) < 9):
                    print("CONNECT {}".format(random.choice([1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3])))
                elif (len(self.current_player.finished) < 12):
                    print("CONNECT {}".format(random.choice([1, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3])))
                else:
                    print("CONNECT {}".format(random.choice([1, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3])))
                    # print("CONNECT {}".format(1))
        else:
            self.current_player.plan = Plans.DIAGNOSE_SAMPLES
            debug('******************change plan({})**********************'.format(self.current_player.plan))
            self._action()

    def _diagnose_samples(self):
        if self.current_player.target != 'DIAGNOSIS' and len(self.current_player.samples) > 0:
            self._move('DIAGNOSIS')
        elif len(self.current_player.samples) > 0:
            for sample_id, player_sample in self.current_player.samples.items():
                if player_sample.molecules_cost.get_count() < 0:
                    print("CONNECT {}".format(player_sample.sample_id))
                    return
            else:
                self.current_player.plan = Plans.CHECK_SAMPLES
                debug(
                    '******************change plan({})**********************'.format(self.current_player.plan))
                self._action()
        else:
            self.current_player.plan = Plans.COLLECT_SAMPLES
            self._action()

    def _check_samples(self):  # todo chose easiest to finish
        if len(self.current_player.samples) > 0:
            for sample_id, player_sample in self.current_player.samples.items():
                debug('_can_finish', self._can_finish(player_sample))
                if (self._can_finish(player_sample)):  # self.can_finish(player_sample)
                    self.current_player.plan = Plans.COLLECT_SAMPLES_MOLECULES
                    self.current_player.target_sample = player_sample
                    self._action()
                    return
                elif self.current_player.target == 'DIAGNOSIS':
                    print("CONNECT {}".format(sample_id))
                    return
            else:
                if self.current_player.target != 'DIAGNOSIS' and len(
                        self.current_player.samples) == self.current_player.care_samples:
                    self.current_player.plan = Plans.COLLECT_SAMPLES
                    self._move('DIAGNOSIS')
                else:
                    self.current_player.plan = Plans.COLLECT_SAMPLES
                    debug('******************change plan({})**********************'.format(
                        self.current_player.plan))
                    self._action()

        else:
            self.current_player.plan = Plans.COLLECT_SAMPLES
            self._action()

    def _collect_sample_molecules(self):
        if len(self.current_player.samples) > 0:
            if self.current_player.target != 'MOLECULES':
                self._move('MOLECULES')
            else:
                # todo: check can finish
                debug('_can_finish', self._can_finish(self.current_player.target_sample))
                if (self._can_finish(self.current_player.target_sample)):
                    for key, value in self.current_player.target_sample.molecules_cost.data.items():
                        if self.current_player.need_more(key, value):
                            print("CONNECT {}".format(key))
                            return
                    else:
                        self.current_player.plan = Plans.FINISH_SAMPLE
                        debug('******************change plan({})**********************'.format(
                            self.current_player.plan))
                        self._action()
                else:
                    self.current_player.plan = Plans.CHECK_SAMPLES
                    debug('******************change plan({})**********************'.format(
                        self.current_player.plan))
                    self._action()

        else:
            self.current_player.plan = Plans.COLLECT_SAMPLES
            debug('******************change plan({})**********************'.format(self.current_player.plan))
            self._action()

    def _finish_samples(self):
        if self.current_player.target != 'LABORATORY':
            self._move('LABORATORY')
            return
        else:
            print("CONNECT {}".format(self.current_player.target_sample.sample_id))
            self.current_player.finished.append(self.current_player.target_sample.sample_id)
            self.current_player.target_sample = None
            self.current_player.plan = Plans.CHECK_SAMPLES
            debug('******************change plan({})**********************'.format(self.current_player.plan))
            self.current_player.care_samples = 3
            return

    def _move(self, to):
        print('GOTO {}'.format(to))
        self.current_player.moving = self.MOVING_TABLE[(self.current_player.target, to)]

    def _can_finish(self, sample):
        for key, value in sample.molecules_cost.data.items():
            if value > self.current_player.storage_molecules.data[key] + \
                    self.current_player.expertise_molecules.data[key] + self.molecules.data[key]:
                return False
        return True

    def _can_finish_now(self):
        pass

game = Game()
# game loop
while True:
    game.run()