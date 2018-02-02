import sys
import math

DEBUG = True


def debug(*args):
    if (DEBUG):
        print(args, file=sys.stderr)  # Bring data on patient samples from the diagnosis machine to the laboratory with enough molecules to produce medicine!

class Project:
    def __init__(self, data):
        self.a, self.b, self.c, self.d, self.e = [int(j) for j in data.split()]

class Robot:
    def put_data(self, data):
        self.target, eta, score, storage_a, storage_b, storage_c, storage_d, storage_e, expertise_a, expertise_b, expertise_c, expertise_d, expertise_e = input().split()
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

class Molecules:
    def put_data(self, data):
        self.available_a, self.available_b, self.available_c, self.available_d, self.available_e = [int(j) for j in data.split()]

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
        for i in range(self.players_count):
            self.players.append(Robot())
            # debug('projects list', self.projects)

    def run(self):
        for i in range(self.players_count):
            self.players[i].put_data(input())
        self.molecules.put_data(input())
        self.sample_count = int(input())
        self.samples.clear()
        for i in range(self.sample_count):
            self.samples.append(Sample(input()))

game = Game()
# game loop
while True:
    game.run()
    print("GOTO DIAGNOSIS")