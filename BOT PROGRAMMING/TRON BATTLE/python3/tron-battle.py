# https://github.com/killruana/codingame/blob/master/tron/tron.py
# https://www.codingame.com/ide/puzzle/tron-battle
#!/usr/bin/env python3
#-*- coding: utf8 -*-

import logging
import sys


###############################################################################
# Vector2
###############################################################################
class Vector2:
    """Vecteur 2"""
    def __init__(self, x=0, y=None):
        if y is None:
            y = x

        self.x = x
        self.y = y

    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        else:
            raise IndexError("list index out of range")

    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        else:
            raise IndexError("list index out of range")

    def __add__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)
        else:
            return Vector2(self.x + other, self.y + other)

    def __sub__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x - other.x, self.y - other.y)
        else:
            return Vector2(self.x - other, self.y - other)

    def __mul__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x * other.x, self.y * other.y)
        else:
            return Vector2(self.x * other, self.y * other)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return "{%s, %s}" % (self.x, self.y)

    def __repr__(self):
        return "Vector2(%r, %r)" % (self.x, self.y)

    def to_direction(self):
        if self.x < 0:
            return Vector2.DIRECTION_LEFT
        elif self.x > 0:
            return Vector2.DIRECTION_RIGHT
        elif self.y < 0:
            return Vector2.DIRECTION_UP
        elif self.y > 0:
            return Vector2.DIRECTION_DOWN
        else:
            return Vector2.DIRECTION_NONE

    def to_direction_string(self):
        if self.x < 0:
            return "LEFT"
        elif self.x > 0:
            return "RIGHT"
        elif self.y < 0:
            return "UP"
        elif self.y > 0:
            return "DOWN"
        else:
            return "NONE"

    def copy(self):
        return Vector2(self.x, self.y)


# Quelques vecteurs utiles
Vector2.ZERO = Vector2(0)
Vector2.ONE = Vector2(1)
Vector2.MINUS_ONE = Vector2(-1)

Vector2.DIRECTION_NONE = Vector2(0)
Vector2.DIRECTION_LEFT = Vector2(-1, 0)
Vector2.DIRECTION_RIGHT = Vector2(1, 0)
Vector2.DIRECTION_UP = Vector2(0, -1)
Vector2.DIRECTION_DOWN = Vector2(0, 1)


###############################################################################
# Inputs handlers
###############################################################################
class InputHandler:
    def read(self):
        """Récupères les informations nécessaires au jeu
        La structure retournée doit ressembler à ça :
        {
            'players_count': <int: number of players>,
            'my_id': <int: our player id>
            'movements': {
                <int: player id>: {
                    'begin': <Vector2, begin of movement>,
                    'end': <Vector2, end of movement>
                },
                ...
            }
        }
        """
        raise NotImplementedError("Abstract method")


class StreamInputHandler(InputHandler):
    def __init__(self, stream=sys.stdin):
        self.stream = stream

    def read(self):
        input_data = {}

        line = self.stream.readline().split()
        input_data['players_count'] = int(line[0])
        input_data['my_id'] = int(line[1])

        input_data['movements'] = {}
        for player_id in range(input_data['players_count']):
            line = self.stream.readline().split()
            input_data['movements'][player_id] = {
                'begin': Vector2(int(line[0]), int(line[1])),
                'end': Vector2(int(line[2]), int(line[3]))
            }

        return input_data


###############################################################################
# Ouputs handler
###############################################################################
class OutputHandler:
    def write(self, direction):
        raise NotImplementedError("Abstract method")


class StreamOutputHandler:
    def __init__(self, stream=sys.stdout):
        self.stream = stream

    def write(self, direction):
        self.stream.write(direction + "\n")
        self.stream.flush()


###############################################################################
# Players
###############################################################################
class Player:
    """Un joueur"""
    def __init__(self, id=0, its_me=False):
        self.id = id
        self.its_me = its_me
        self.position = None
        self.has_lost = False
        self.previous_direction = None


class Players:
    """Une collection de joueurs"""
    def __init__(self):
        self.players = {}

    def add(self, player):
        self.players[player.id] = player

    def remove(self, player_id):
        del self.players[player_id]

    def get(self, player_id):
        return self.players[player_id]

    def exists(self, player_id):
        return player_id in self.players

    def __len__(self):
        return len(self.players)

    def get_me(self):
        for player_id, player in self.players.items():
            if player.its_me:
                return player

        return None


###############################################################################
# AI
###############################################################################
class ArtificialIntelligence:
    def update(self, arena):
        raise NotImplementedError("Abstract method")


class MaevaArtificialIntelligence(ArtificialIntelligence):
    """Tout comme Maeva, cette IA n'est pas très futée..."""
    def update(self, arena):
        return "LEFT"


class SheldonArtificialIntelligence(ArtificialIntelligence):
    """Bazinga!"""
    def update(self, arena):
        me = arena.players.get_me()

        direction = me.direction
        if direction == Vector2.DIRECTION_NONE:
            direction = Vector2.DIRECTION_UP

        for i in range(4):
            logging.getLogger().debug("trying direction %s (%s)",
                                      direction.to_direction_string(),
                                      direction)
            position = me.position + direction
            if arena.is_valid_position(position):
                return direction.to_direction_string()

            if direction == Vector2.DIRECTION_UP:
                direction = Vector2.DIRECTION_RIGHT
            elif direction == Vector2.DIRECTION_RIGHT:
                direction = Vector2.DIRECTION_DOWN
            elif direction == Vector2.DIRECTION_DOWN:
                direction = Vector2.DIRECTION_LEFT
            elif direction == Vector2.DIRECTION_LEFT:
                direction = Vector2.DIRECTION_UP

        return "DAMNIT"


###############################################################################
# Arena
###############################################################################
class Arena:
    """L'arène de jeu"""
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.reset_board()

        self.players = Players()

    def reset_board(self):
        self.board = [[-1 for x in range(self.width)] for y in range(self.height)]

    def dump_board(self):
        return "\n".join(map(lambda line: "".join(map(lambda val: str(val) if val >= 0 else '.', line)), self.board))

    def update(self, input_data):
        for player_id, movement in input_data['movements'].items():
            begin = movement['begin']
            end = movement['end']

            if not self.players.exists(player_id):
                logging.getLogger().info("creating player %i", player_id)
                player = Player(player_id, player_id == input_data['my_id'])
                self.players.add(player)
            else:
                player = self.players.get(player_id)

            if begin == end == Vector2.MINUS_ONE:
                if not player.has_lost:
                    logging.getLogger().info("player %i has lost", player_id)

                    player.has_lost = True
                    self.remove_walls_of_player(player)
            else:
                self.move_player(player, begin, end)

    def remove_walls_of_player(self, player):
        for x in range(self.width):
            for y in range(self.height):
                if self.board[y][x] == player.id:
                    self.board[y][x] = -1

    def move_player(self, player, begin, end):
        diff = end - begin
        logging.getLogger().info("moving player %i from %s to %s (%s)", player.id, begin, end, diff)

        player.position = end
        self.board[end.y][end.x] = player.id
        player.direction = diff.to_direction()

    def is_valid_position(self, position):
        if position.x < 0 or position.x >= self.width or position.y < 0 or position.y >= self.height:
            return False

        if self.board[position.y][position.x] != -1:
            return False

        return True


###############################################################################
# Game
###############################################################################
class Game:
    """Le jeu"""
    def __init__(self):
        self.input_handler = None
        self.arena = None
        self.ai = None

    def run(self):
        """Exécute le jeu"""
        while True:
            self.step()

    def step(self):
        """Exécute une étape du jeu"""
        input_data = self.read_input()
        self.updata_arena(input_data)
        new_direction = self.update_ai()
        self.output_handler.write(new_direction)

    def read_input(self):
        input_data = self.input_handler.read()
        logging.getLogger().debug("read data: %s", input_data)

        return input_data

    def updata_arena(self, input_data):
        self.arena.update(input_data)

    def update_ai(self):
        direction = self.ai.update(self.arena)
        logging.getLogger().debug("new direction: %s", direction)

        return direction


###############################################################################
#
###############################################################################
def main():
    CONFIG = {
        # Configuration des flux d'entrées/sorties
        'stream': {
            'input': sys.stdin,
            'output': sys.stdout,
            'debug': sys.stderr,
        },


        # Configuration de la journalisation
        'logging': {
            'level': logging.CRITICAL,
        },


        # Configuration de l'arène
        'arena': {
            'width': 30,
            'height': 20,
        },


        # Configuration de l'ia
        'ai': {
            'selected': 'sheldon',
        },


        # Configuration des gestionnaires d'entrées
        'input_handler': {
            'selected': 'stream',
        },


        # Configuration des gestionnaires de sorties
        'output_handler': {
            'selected': 'stream',
        },


        # Game
        'game': {
            'loop_count': -1,  # infini si <= 0
            'dump_board_after_step': True,
        },
    }

    # Mise en place du système de journalisation
    logger = logging.getLogger()
    logger.setLevel(CONFIG['logging']['level'])

    formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')

    stream_handler = logging.StreamHandler(CONFIG['stream']['debug'])
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # Préparation du jeu
    logger.debug("Initializations...")
    game = Game()

    # Gestionnaire d'entrées
    input_handler = None
    if CONFIG['input_handler']['selected'] == 'stream':
        input_handler = StreamInputHandler(CONFIG['stream']['input'])
    else:
        logger.error('invalid input handler "%s"', CONFIG['input_handler']['selected'])
        sys.exit()
    game.input_handler = input_handler

    # Gestionnaire de sorties
    output_handler = None
    if CONFIG['output_handler']['selected'] == 'stream':
        output_handler = StreamOutputHandler(CONFIG['stream']['output'])
    else:
        logger.error('invalid output handler "%s"', CONFIG['output_handler']['selected'])
        sys.exit()
    game.output_handler = output_handler

    # AI
    ai = None
    if CONFIG['ai']['selected'] == 'maeva':
        ai = MaevaArtificialIntelligence()
    elif CONFIG['ai']['selected'] == 'sheldon':
        ai = SheldonArtificialIntelligence()
    else:
        logger.error('invalid ai "%s"', CONFIG['ai']['selected'])
        sys.exit()
    game.ai = ai

    # Arène
    arena = Arena(CONFIG['arena']['width'], CONFIG['arena']['height'])
    game.arena = arena

    # Exécution du jeu - PAN!
    loop_count = 1
    while True:
        logging.getLogger().info("running game step %i", loop_count)

        game.step()

        if CONFIG['game']['dump_board_after_step']:
                logger.debug("arena:\n%s", game.arena.dump_board())

        loop_count += 1
        if CONFIG['game']['loop_count'] > 0 and loop_count > CONFIG['game']['loop_count']:
            break


if __name__ == '__main__':
    main()