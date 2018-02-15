import sys
import math

DEBUG = True


def debug(*args):
    if (DEBUG):
        print(args, file=sys.stderr)  # Bring data on patient samples from the diagnosis machine to the laboratory with enough molecules to produce medicine!


class Molecules:
    MOLECULES = ['A', 'B', 'C', 'D', 'E']

    def __init__(self, data=None):
        if data is None:
            self.data = {key: 0 for key in self.MOLECULES}
        else:
            self.put_data(data)

    def put_data(self, data):
        # debug('put storage', data)
        self.data = dict(zip(self.MOLECULES, [int(j) for j in data]))
        # debug('result', self.data)

    def get_count(self):
        return sum(self.data.values())

    def get_min_key(self):
        return min(self.data, key=lambda k: self.data[k])


class Project:
    def __init__(self, data):
        self.data = Molecules(data.split())


class Robot:
    storage_molecules = Molecules()
    expertise_molecules = Molecules()

    def put_data(self, data):
        self.target, eta, score, storage_a, storage_b, storage_c, storage_d, storage_e, expertise_a, expertise_b, expertise_c, expertise_d, expertise_e = data
        self.eta = int(eta)
        self.score = int(score)
        debug('robot data', [storage_a, storage_b, storage_c, storage_d, storage_e])
        self.storage_molecules.put_data([storage_a, storage_b, storage_c, storage_d, storage_e])

        self.expertise_molecules.put_data([expertise_a, expertise_b, expertise_c, expertise_d, expertise_e])
        # debug(self.target)


class Plans:
    COLLECT_MOLECULES = 0  # just grab 8 molecules
    COLLECT_SAMPLES_MOLECULES = 1  # grab for samples
    COLLECT_SAMPLES = 2
    DIAGNOSE_SAMPLES = 3


class Player(Robot):
    plan = Plans.COLLECT_MOLECULES


class Sample:
    def __init__(self, data):
        sample_id, carried_by, rank, self.expertise_gain, health, cost_a, cost_b, cost_c, cost_d, cost_e = data.split()
        self.sample_id = int(sample_id)
        self.carried_by = int(carried_by)
        self.rank = int(rank)
        self.health = int(health)
        self.molecules_cost = Molecules([cost_a, cost_b, cost_c, cost_d, cost_e])


class Game:
    projects = []
    players_count = 2
    my_player_id = 0
    molecules = Molecules()
    players = []
    sample_count = 0
    samples = []

    def __init__(self):
        self.project_count = int(input())
        # debug(self.project_count)
        for i in range(self.project_count):
            self.projects.append(Project(input()))
        self.players.append(Player())
        for i in range(1, self.players_count):
            self.players.append(Robot())
        self.current_player = self.players[self.my_player_id]

    def run(self):
        self._collect_data()
        self._action()

    def _collect_data(self):
        for i in range(self.players_count):
            self.players[i].put_data(input().split())
        self.molecules.put_data(input().split())
        self.sample_count = int(input())
        self.samples.clear()
        for i in range(self.sample_count):
            self.samples.append(Sample(input()))
        self.player_samples = self._get_player_samples(self.my_player_id)

    def _get_player_samples(self, player_id):
        return [x for x in self.samples if x.carried_by == player_id]

    def _action(self):
        debug(self.current_player.target)
        if self.current_player.plan == Plans.COLLECT_MOLECULES:
            self._collect_molecules()
        elif self.current_player.plan == Plans.COLLECT_SAMPLES:
            self._collect_samples()
        elif self.current_player.plan == Plans.COLLECT_SAMPLES:
            self._collect_samples()
        else:
            print("WAIT")
        # elif
        # elif self.current_player.target == 'SAMPLES':
        #    self._action_samples()
        # elif self.current_player.target == 'DIAGNOSIS':
        #    self._action_diagnosis()
        # elif self.current_player.target == 'MOLECULES':
        #    self._action_molecules()
        # elif self.current_player.target == 'LABORATORY':
        #    self._action_laboratory()
        # else:
        #    print("GOTO SAMPLES")

    def _collect_molecules(self):
        if self.current_player.target != 'MOLECULES':
            print("GOTO MOLECULES")
            return
        elif self.current_player.storage_molecules.get_count() < 10 and self.molecules.get_count() > 0:
            debug(self.current_player.storage_molecules.data)
            storage_molecules = sorted(self.current_player.storage_molecules.data,
                                       key=self.current_player.storage_molecules.data.get)
            debug(storage_molecules)
            for key in storage_molecules:
                if self.molecules.data[key] > 0:
                    print("CONNECT {}".format(key))
                    return
        print("GOTO SAMPLES")
        self.current_player.plan = Plans.COLLECT_SAMPLES
        return

    def _collect_samples(self):
        if len(self.player_samples) < 3:
            print("CONNECT {}".format(3 - len(self.player_samples)))
        else:
            print("GOTO DIAGNOSIS")
            self.current_player.plan = Plans.DIAGNOSE_SAMPLES


game = Game()
# game loop
while True:
    game.run()