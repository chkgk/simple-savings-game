from otree.api import Currency as c, currency_range, expect, Bot
from . import *


class PlayerBot(Bot):
    def play_round(self):
        yield Page1, {'risk_choice': '1'}
        yield Page2, {'finlit_q1': 'more_102', 'finlit_q2': 'same', 'finlit_q3': 'false'}
        yield Page3, {'time_preference_1': 'A', 'time_preference_2': 'A', 'time_preference_3': 'A', 'time_preference_4': 'B', 'time_preference_5': 'B', 'time_preference_6': 'B'}
        yield Page4, {'compound_q1': '1100', 'compound_q2': 'more_2000', 'compound_q3': 'more_1150', 'compound_q4': '32000'}
        yield Page5, {'age': 35, 'gender': 'male', 'education': 'master', 'investment_experience': 'very_exp'}
        yield Submission(Summary, check_html=False)
        