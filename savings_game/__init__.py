from otree.api import *
import random

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'savings_game'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 12 + 1  # last one is not actually played, we just need it for calculations
    
    INITIAL_CASH = 400
    INITIAL_FOOD = 0
    INITIAL_SALARY = 4.00
    INITIAL_FOOD_PRICE = 4.20

    # note, these are all monthly
    SAVINGS_INTEREST_RATE = 0.019
    ASSET_EXPECTED_RETURN = 0.06
    ASSET_STANDARD_DEVIATION = 0.02
    INFLATION_RATE = {
        'low': 0.05,
        'high': 0.10
    }

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    inflation_regime = models.StringField()
    food_purchase = models.IntegerField(label="How much food do you want to buy?")
    risky_investment = models.IntegerField(label="How much do you want to invest in the asset?")
    
    cash = models.CurrencyField()
    food = models.IntegerField()
    
    salary = models.CurrencyField(default=0)
    interest_payment = models.CurrencyField(default=0)
    asset_payment = models.CurrencyField(default=0)
    
# FUNCTIONS

def creating_session(subsession):
    for p in subsession.get_players():
        p.inflation_regime = 'low'
        if p.round_number == 1:
            p.cash = C.INITIAL_CASH
            p.food = C.INITIAL_FOOD

def get_food_price(player):
    if player.round_number == 1:
        return C.INITIAL_FOOD_PRICE
    return C.INITIAL_FOOD_PRICE * (1 + C.INFLATION_RATE[player.inflation_regime]) ** (player.round_number - 1)

def js_and_template_vars(player):
    return {
        'food_price': cu(get_food_price(player)),
        'cash': player.cash,
        'food': player.food,
        'salary': cu(C.INITIAL_SALARY),
        'interest_rate': C.SAVINGS_INTEREST_RATE * 100,
        'asset_expected_return': C.ASSET_EXPECTED_RETURN * 100,
        'max_rounds': C.NUM_ROUNDS - 1
    }

def get_asset_payment(investment):
    mu = C.ASSET_EXPECTED_RETURN
    sigma = C.ASSET_STANDARD_DEVIATION
    sample = random.gauss(mu, sigma)
    return investment * sample

# PAGES
class Savings(Page):
    form_model = 'player'
    form_fields = ['food_purchase', 'risky_investment']
    
    def is_displayed(player):
        return player.round_number < C.NUM_ROUNDS  # do not play the last round, just use if for calculations
    
    def before_next_page(player, timeout_happened):
        current_cash = player.cash
        food_expense = player.food_purchase * get_food_price(player)
        asset_expense = player.risky_investment
        unspent_cash = current_cash - food_expense - asset_expense
        
        # here we need to check if the player is bankrupt (but also check if they can still purchase at least one unit of food / have one unit of food left)
        
        # calculate new cash
        interest_payment = cu(unspent_cash * C.SAVINGS_INTEREST_RATE)
        asset_payment = cu(get_asset_payment(player.risky_investment))
        salary = cu(C.INITIAL_SALARY)
        new_cash = unspent_cash + salary + interest_payment + asset_payment
        
        # calculate new food
        new_food = player.food - 1 + player.food_purchase
        
        # write variables for next round
        next_player = player.in_round(player.round_number + 1)
        next_player.cash = new_cash
        next_player.food = new_food
        next_player.asset_payment = asset_payment
        next_player.salary = salary
        next_player.interest_payment = interest_payment
            
    
    @staticmethod
    def js_vars(player):
        return js_and_template_vars(player)
    
    @staticmethod
    def vars_for_template(player):
        return js_and_template_vars(player)


class Results(Page):
    def is_displayed(self):
        return self.round_number == C.NUM_ROUNDS
    
    def vars_for_template(player):
        total_interest_payments = 0
        total_asset_payments = 0
        total_salaries = 0
        
        for p in player.in_all_rounds():
            total_interest_payments += p.interest_payment
            total_asset_payments += p.asset_payment
            total_salaries += p.salary
            
        return {
            'total_interest_payments': total_interest_payments,
            'total_asset_payments': total_asset_payments,
            'total_salaries': total_salaries,
            'leftover_food': player.food,
            'final_cash': player.cash
        }


page_sequence = [Savings, Results]
