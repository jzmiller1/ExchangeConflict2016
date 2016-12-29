from collections import Counter
import random

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


class GameConfig:
    def __init__(self,
                 player=PlayerConfig(),
                 ):
        self.player = player


class Player:
    def __init__(self, game, name, credits, current_node):
        self.universe = game
        self.name = name
        self.wallet = credits
        self.ship_current = None
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
        self.players[name] = Player(self,
                                    name,
                                    credits=self.config.player.initial_credits,
                                    current_node=self.config.player.initial_sector_id)