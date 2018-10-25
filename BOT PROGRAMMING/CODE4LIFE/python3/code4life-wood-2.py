import sys
import math

DEBUG = True


def debug(*args):
    if (DEBUG):
        print(args, file
              =sys.stderr)  # Bring data on patient samples from the diagnosis machine to the laboratory with enough molecules to produce medicine!


class Project:
    def __init__(self, data):
        self.a, self.b, self.c, self.d, self.e = [int(j) for j in data.split()]


class Robot:
    def put_data(self, data):
        self.target, eta, score, storage_a, storage_b, storage_c, storage_d, storage_e, expertise_a, expertise_b, expertise_c, expertise_d, expertise_e = data.split()
        self.eta = int(eta)
        self.score = int(score)
        self.storage_a = int(storage_a)
        self.storage_b = int(storage_b)
        self.storage_c = int(storage_c)
        self.storage_d = int(storage_d)
        self.storage_e = int(storage_e)
        self.expertise_a = int(expertise_a)
        self.expertise_b = int(expertise_b)
        self.expertise_c = int(expertise_c)
        self.expertise_d = int(expertise_d)
        self.expertise_e = int(expertise_e)
        debug(self.target)

    def get_molecules(self):
        return {'A': self.storage_a, 'B': self.storage_b, 'C': self.storage_c, 'D': self.storage_d, 'E': self.storage_e}

    def get_molecules_count(self):
        return self.storage_a + self.storage_b + self.storage_c + self.storage_d + self.storage_e


class Player(Robot):
    pass


class Molecules:
    def put_data(self, data):
        self.available_a, self.available_b, self.available_c, self.available_d, self.available_e = [int(j) for j in
                                                                                                    data.split()]


class Sample:
    def __init__(self, data):
        sample_id, carried_by, rank, self.expertise_gain, health, cost_a, cost_b, cost_c, cost_d, cost_e = data.split()
        self.sample_id = int(sample_id)
        self.carried_by = int(carried_by)
        self.rank = int(rank)
        self.health = int(health)
        self.cost_a = int(cost_a)
        self.cost_b = int(cost_b)
        self.cost_c = int(cost_c)
        self.cost_d = int(cost_d)
        self.cost_e = int(cost_e)

    def get_cost(self):
        return {'A': self.cost_a, 'B': self.cost_b, 'C': self.cost_c, 'D': self.cost_d, 'E': self.cost_e}


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
        debug('projects list', self.players)

    def run(self):
        self._collect_data()
        self._action()

    def _collect_data(self):
        for i in range(self.players_count):
            self.players[i].put_data(input())
        self.molecules.put_data(input())
        self.sample_count = int(input())
        self.samples.clear()
        for i in range(self.sample_count):
            self.samples.append(Sample(input()))

    def _get_player_samples(self, player_id):
        return [x for x in self.samples if x.carried_by == player_id]

    def _get_player_molecules(self, player_id):
        return [x for x in self.samples if x.carried_by == player_id]

    def _action(self):
        # debug('samples', self.samples)
        # debug(self.my_player_id)
        current_player = self.players[self.my_player_id]
        player_samples = self._get_player_samples(self.my_player_id)
        if current_player.target == 'START_POS':
            print("GOTO DIAGNOSIS")
        elif current_player.target == 'DIAGNOSIS':
            avaliable_samples = self._get_player_samples(-1)
            if len(player_samples) < 3 and len(avaliable_samples) > 0:
                print("CONNECT {}".format(avaliable_samples[0].sample_id))  # todo: minimum molecules needed
            else:
                print("GOTO MOLECULES")
        elif current_player.target == 'MOLECULES':
            if len(player_samples) > 0:
                molecules_nedded = player_samples[0].get_cost()
                molecules_have = current_player.get_molecules()
                for key, molecule in molecules_nedded.items():
                    if molecule > molecules_have[key]:
                        print("CONNECT {}".format(key))
                        break
                else:
                    print("GOTO LABORATORY")
            else:
                print("GOTO DIAGNOSIS")
        elif current_player.target == 'LABORATORY':
            if len(player_samples) > 0:
                molecules_count = current_player.get_molecules_count()
                if molecules_count > 0:
                    print("CONNECT {}".format(player_samples[0].sample_id))
                else:
                    print("GOTO MOLECULES")
            else:
                print("GOTO DIAGNOSIS")

        else:
            print("GOTO DIAGNOSIS")

        # player_samples = self._get_player_samples(self.my_player_id)
        # debug('player_samples', player_samples)
        # if(len(player_samples)==0 or ):
        # print("GOTO DIAGNOSIS")
        # elif


game = Game()
# game loop
while True:
    game.run()