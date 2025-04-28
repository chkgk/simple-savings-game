from otree.api import Currency as c, currency_range, expect, Bot
from . import *


class PlayerBot(Bot):
    def play_round(self):
        yield Instructions1
        yield Instructions2, {'food_reserve_question': 1}
        yield Instructions3, {'cash_interest_question': 80}
        yield Instructions4, {'cash_balance_question': 140}
        yield Instructions5, {'interest_rate_change_question': 'no', 'food_price_change_question': 'never_decrease'}
        yield TrainingRound1, {'food_purchase': 3, 'risky_investment': 5}
        yield TrainingRound2, {'food_purchase': 2, 'risky_investment': 5}
        yield Instructions6, {'remuneration_question': 'cash'}
        yield Instructions7
