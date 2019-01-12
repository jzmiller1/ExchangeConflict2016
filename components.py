from collections import Counter
import json
import random
import uuid

from utils import bimodal


class Commodity:
    def __init__(self,
                 name,
                 price_distribution_low,
                 price_distribution_high,
                 unit_range_low,
                 unit_range_high,
                 **kwargs):
        self.name = name
        self.price_distribution_low = price_distribution_low
        self.price_distribution_high = price_distribution_high
        self.unit_range_low = unit_range_low
        self.unit_range_high = unit_range_high
        self.units = kwargs.get('units', None)
        self.price_buy = kwargs.get('units', None)
        self.price_sell = kwargs.get('units', None)

    def __repr__(self):
        return "Commodity('{}', {}, {}, {}, {})".format(self.name,
                                                        self.price_distribution_low,
                                                        self.price_distribution_high,
                                                        self.unit_range_low,
                                                        self.unit_range_high)

    def generate(self):
        self.units = random.randint(self.unit_range_low, self.unit_range_high)
        x = round(bimodal(*self.price_distribution_low, *self.price_distribution_high), 0)
        y = round(bimodal(*self.price_distribution_high, *self.price_distribution_low), 0)
        self.price_buy = min(x, y)
        self.price_sell = max(x, y)


class PlayerConfig:
    def __init__(self,
                 initial_sector_id=1,
                 initial_ship_type="merchant_cruiser",
                 initial_credits=5000
                 ):
        self.initial_credits = initial_credits
        self.initial_ship_type = initial_ship_type
        self.initial_sector_id = initial_sector_id


class ShipsConfig:
    def __init__(self, ship_data='data/ships.json'):
        f = open(ship_data, 'r')
        self.types = json.loads(f.read())['types']
        f.close()


class GameConfig:
    def __init__(self,
                 player=PlayerConfig(),
                 ships=ShipsConfig()
                 ):
        self.player = player
        self.ships = ships


class Player:
    def __init__(self, game, name, credits, current_node, ship):
        self.universe = game
        self.name = name
        self.wallet = credits
        self.ship_current = ship
        self.sectors_visited = Counter()
        self.current_node = current_node


class Universe:
    def __init__(self, name, graph, config=GameConfig()):
        self.name = name
        self.graph = graph
        self.config = config
        self.players = {}
        self.ships = {}

    def create_player(self, name):
        """Add a new player to the game"""
        sid = uuid.uuid4()
        self.players[name] = Player(self,
                                    name,
                                    credits=self.config.player.initial_credits,
                                    current_node=self.config.player.initial_sector_id,
                                    ship=sid)
        self.create_ship('merchant_cruiser', sid)

    def create_ship(self, stype, sid):
        ship = {}
        for k, v in self.config.ships.types[stype].items():
            ship[k] = v
        ship['holds_current'] = ship['holds_min']
        ship['cargo'] = {}
        self.ships[sid] = ship
