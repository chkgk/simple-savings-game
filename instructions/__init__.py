from otree.api import *
import random

class C(BaseConstants):
    NAME_IN_URL = 'instructions'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    PAYMENT_PROBABILITY = 0.1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    food_reserve_question = models.IntegerField(
        label="How many units of food are consumed each month?",
        choices=[(3, '3'), (0, '0'), (1, '1'), (13, '13')],
        widget=widgets.RadioSelect,
    )
    cash_interest_question = models.IntegerField(
        label="If your cash is $100 at the beginning of a month and the only expenditure is an investment of $20 into the asset, what amount will earn 1.9% interest?",
        choices=[(100, '$100'), (120, '$120'), (20, '$20'), (80, '$80')],
        widget=widgets.RadioSelect,
    )
    cash_balance_question = models.IntegerField(
        label="Suppose you had $100 in cash last month. If you earn $10 in interest, receive $20 in monthly salary, get $40 in Total Asset Payment, and spend $30 on food, what will your cash be before continuing to the next month?",
        choices=[(100, '$100'), (170, '$170'), (200, '$200'), (140, '$140')],
        widget=widgets.RadioSelect,
    )
    interest_rate_change_question = models.StringField(
        label="Can the Interest Rate change during the game?",
        choices=[
            ('yes', 'Yes'),
            ('no', 'No'),
            ('depends_cash', 'It depends how much Cash you have'),
            ('depends_total', 'It depends how much is in Total Cash'),
        ],
        widget=widgets.RadioSelect,
    )
    food_price_change_question = models.StringField(
        label="Can the price of Food change?",
        choices=[
            ('never_decrease', 'It can never decrease'),
            ('never_increase', 'It can never increase'),
            ('can_both', 'It can increase and decrease.'),
            ('cannot_change', 'It cannot change'),
        ],
        widget=widgets.RadioSelect,
    )
    remuneration_question = models.StringField(
        label="The final value of which of these balances determines your performance-based remuneration for the game?",
        choices=[
            ('investment', 'Asset investment'),
            ('food', 'Food Reserves'),
            ('cash', 'Cash'),
            ('interest', 'Interest earned'),
        ],
        widget=widgets.RadioSelect,
    )
    food_price_estimate_example = models.StringField()

    food_purchase = models.IntegerField()
    risky_investment = models.CurrencyField()


# Functions
def creating_session(subsession):
    for p in subsession.get_players():
        if p.round_number == 1:
            p.participant.vars["pay_for_real"] = random.random() <= C.PAYMENT_PROBABILITY
            # p.participant.vars["treatment"] = random.choice(["high-high", "high-low", "low-high", "low-low"])

def food_reserve_question_error_message(player, value):
    if value != 1:
        return "Please review the instructions carefully: You must consume exactly 1 unit of Food each month."
    return None

def cash_interest_question_error_message(player, value):
    if value != 80:
        return "Please review the instructions carefully: Only the uninvested Cash earns 1.9% interest."
    return None

def cash_balance_question_error_message(player, value):
    if value != 140:
        return "Please review the instructions: Your Cash is increased by income (interest, salary, asset payment) and reduced by expenses (food and investment costs)."
    return None

def interest_rate_change_question_error_message(player, value):
    if value != "no":
        return "Remember: The Interest Rate stays constant throughout the entire game."
    return None

def food_price_change_question_error_message(player, value):
    if value != "never_decrease":
        return "Please review: The price of food can increase during the game, but it can never decrease."
    return None

def remuneration_question_error_message(player, value):
    if value != "cash":
        return "Careful: Only your final Cash balance determines your study earnings."
    return None


# Pages
class Instructions1(Page):
    pass


class Instructions2(Page):
    form_model = 'player'
    form_fields = ['food_reserve_question']


class Instructions3(Page):
    form_model = 'player'
    form_fields = ['cash_interest_question']


class Instructions4(Page):
    form_model = 'player'
    form_fields = ['cash_balance_question']


class Instructions5(Page):
    form_model = 'player'
    form_fields = ['interest_rate_change_question', 'food_price_change_question']


class TrainingRound1(Page):
    form_model = 'player'
    form_fields = ['food_purchase', 'risky_investment']

    def error_message(player, values):
        if values['food_purchase'] != 3 or values['risky_investment'] != cu(5):
            return "Please buy exactly 3 units of food and invest exactly 5 $."
        return None

    @staticmethod
    def vars_for_template(player):
        return {
            'training': True,
            'task': 'Buy 3 units of food and invest $5.',
            'cash': "30.00",
            'food': "0",
            'salary': "8.00",
            'interest_payment': "0.00",
            'asset_payment': "0.00",
            'realized_asset_payoff': None,
            'food_price': "4.20",
            'interest_rate': "1.9",
            'max_rounds': 12,
        }

    @staticmethod
    def js_vars(player):
        return {
            'food_price': 4.20,
            'cash': 30,
            'food': 0,
        }

class TrainingRound2(Page):
    form_model = 'player'
    form_fields = ['food_purchase', 'risky_investment']
    template_name = 'instructions/TrainingRound2.html'

    def error_message(player, values):
        food_price = 4.20
        food_expense = values['food_purchase'] * food_price
        total_expense = food_expense + values['risky_investment']
        if values['food_purchase'] != 2 or abs(food_expense - 8.40) > 0.05 or abs(total_expense - 13.40) > 0.05:
            return "Please buy 2 units of food and invest $5 so that food expenses are $8.40 and total expenses are $13.40."
        return None

    @staticmethod
    def vars_for_template(player):
        return {
            'training': True,
            'task': 'Now buy 2 units of food and invest $5 so that food expenses are $8.40 and Total expenses are $13.40.',
            'cash': "28.64",
            'food': "2",
            'salary': "8.00",
            'interest_payment': "0.24",
            'asset_payment': "8.00",
            'realized_asset_payoff': "1.60",
            'food_price': "4.20",
            'interest_rate': "1.9",
            'max_rounds': 12,
        }

    @staticmethod
    def js_vars(player):
        return {
            'food_price': 4.20,
            'cash': 30,
            'food': 2,  # in TrainingRound2 the player starts with 2 units
        }


class Instructions6(Page):
    form_model = 'player'
    form_fields = ['remuneration_question']


class Instructions7(Page):
    pass


class Instructions8(Page):
    pass


page_sequence = [
    Instructions1,
    Instructions2,
    Instructions3,
    Instructions4,
    Instructions5,
    TrainingRound1,
    TrainingRound2,
    Instructions6,
    Instructions7
]
