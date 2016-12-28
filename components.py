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
