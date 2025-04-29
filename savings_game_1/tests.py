from otree.api import Currency as c, currency_range, expect, Bot
from . import *
from savings_game_config import TEST_PURCHASE_PLAN, TEST_FINAL_CASH_AMOUNTS


class PlayerBot(Bot):
    def play_round(self):
        if self.round_number < C.NUM_ROUNDS:
            assert self.player.cash == TEST_FINAL_CASH_AMOUNTS[self.player.inflation_regime][self.round_number - 1]
        
        if self.round_number < C.NUM_ROUNDS:
            yield Savings, TEST_PURCHASE_PLAN[self.round_number - 1]
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
        
    