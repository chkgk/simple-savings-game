from otree.api import Currency as c, currency_range, expect, Bot
from . import *

PURCHASE_PLAN = [
    {'food_purchase': 1, 'risky_investment': c(5)}
    for _ in range(12)
]

class PlayerBot(Bot):
    def play_round(self):
        if self.round_number < C.NUM_ROUNDS:
            yield Savings, PURCHASE_PLAN[self.round_number - 1]
        if self.round_number == 6:
            yield FoodPriceEstimate6, {
                'food_price_estimate_6': 10
            }
        if self.round_number == 12:
            yield FoodPriceEstimate12, {
                'food_price_estimate_12': 15
            }
        if self.round_number == C.NUM_ROUNDS:
            yield Results
        