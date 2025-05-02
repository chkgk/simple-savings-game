from otree.api import *
from savings_game_config import SAVINGS_GAME_CONFIG
import random

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'savings_game_1'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 12 + 1  # last one is not actually played, we just need it for calculations
    GAME_ROUND = 1
    

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    food_purchase = models.IntegerField()
    risky_investment = models.FloatField()
    
    dead = models.BooleanField(default=False)
    death_round = models.IntegerField()
    death_reason = models.StringField()
    
    cash = models.FloatField()
    food = models.IntegerField()
    
    salary = models.FloatField(default=0)
    food_expense = models.FloatField(default=0)
    interest_payment = models.FloatField(default=0)
    asset_payment = models.FloatField(default=0)
    realized_asset_payoff = models.FloatField(blank=True)

    food_price_estimate_6 = models.FloatField(label="How much do you think the price of Food changed during the previous 6 months in percentage terms?")
    food_price_estimate_12 = models.FloatField(label="How much do you think the price of Food changed during the previous 6 months in percentage terms?")
    
    initial_cash = models.FloatField()
    initial_food = models.IntegerField()
    initial_salary = models.FloatField()
    initial_food_price = models.FloatField()
    savings_interest_rate = models.FloatField()
    asset_expected_return = models.FloatField()
    asset_standard_deviation = models.FloatField()
    inflation_rate = models.FloatField()
    inflation_regime = models.StringField()
    
# FUNCTIONS
def get_regime(player):
    treatment = player.participant.vars.get('treatment', None)
    if treatment is None:
        treatment = random.choice(["high-high", "high-low", "low-high", "low-low"])
        player.participant.vars["treatment"] = treatment
    
    pay_round = player.participant.vars.get('pay_round', None)
    if pay_round is None:
        pay_round = random.choice([1, 2])
        player.participant.vars["pay_round"] = pay_round
    
    app_regimes = treatment.split('-')
    return app_regimes[C.GAME_ROUND-1]

def creating_session(subsession):    
    for p in subsession.get_players():
        p.inflation_regime = get_regime(p)
        config = SAVINGS_GAME_CONFIG[p.inflation_regime]
        p.initial_cash = config['INITIAL_CASH']
        p.initial_food = config['INITIAL_FOOD']
        p.initial_salary = config['INITIAL_SALARY']
        p.initial_food_price = config['INITIAL_FOOD_PRICE']
        p.savings_interest_rate = config['SAVINGS_INTEREST_RATE']
        p.inflation_rate = config['INFLATION_RATE']
        if p.round_number == 1:
            p.cash = p.initial_cash
            p.food = p.initial_food

def get_food_price(player):
    if player.round_number == 1:
        return player.initial_food_price
    return player.initial_food_price * (1 + player.inflation_rate) ** (player.round_number - 1)

def js_and_template_vars(player):
    rap = player.field_maybe_none('realized_asset_payoff')
    if rap is None or player.asset_payment == 0:
        realized_asset_payoff = '-'
    else:
        realized_asset_payoff = f"${rap:.2f}"
    return {
        'food_price': get_food_price(player),
        'cash': player.cash,
        'food': player.food,
        'salary': player.initial_salary,
        'interest_rate': player.savings_interest_rate * 100,
        'max_rounds': C.NUM_ROUNDS - 1,
        'realized_asset_payoff': realized_asset_payoff,
    }


def get_asset_payment(player):
    payoff_list = SAVINGS_GAME_CONFIG[player.inflation_regime]['ASSET_PAYOFFS']
    realized_payoff = payoff_list[player.round_number - 1]
    return realized_payoff, realized_payoff * player.risky_investment

# PAGES
class Savings(Page):
    form_model = 'player'
    form_fields = ['food_purchase', 'risky_investment']
    template_name = 'savings_game_common/Savings.html'
    
    def is_displayed(player):
        # do not play the last round, just use if for calculations
        # make sure to skip if player is dead
        return player.round_number < C.NUM_ROUNDS and not player.in_round(C.NUM_ROUNDS).dead
    
    def before_next_page(player, timeout_happened):        
        current_cash = player.cash
        food_price = get_food_price(player)
        food_expense = player.food_purchase * food_price
        asset_expense = player.risky_investment
        unspent_cash = current_cash - food_expense - asset_expense
        player.food_expense = food_expense
        
        # calculate new food
        new_food = player.food - 1 + player.food_purchase
        
        # calculate new cash
        interest_payment = unspent_cash * player.savings_interest_rate
        asset_realization, asset_payoff = get_asset_payment(player)
        asset_payment = asset_payoff
        salary = player.initial_salary
        new_cash = unspent_cash + salary + interest_payment + asset_payment
        
        # new food price
        new_food_price = food_price * (1 + player.inflation_rate)
        
        final_round_player = player.in_round(C.NUM_ROUNDS)
        
        if new_food < 0:
            # player died
            final_round_player.dead = True
            final_round_player.death_reason = "negative food"
            final_round_player.death_round = player.round_number
            
        
        if new_food == 0 and new_cash < new_food_price:
            final_round_player.dead = True
            final_round_player.death_reason =  "not enough cash for future consumption"
            final_round_player.death_round = player.round_number
            new_cash = 0
        
        # write variables for next round
        next_player = player.in_round(player.round_number + 1)
        next_player.cash = new_cash
        next_player.food = new_food
        next_player.asset_payment = asset_payment
        next_player.realized_asset_payoff = asset_realization
        next_player.salary = salary
        next_player.interest_payment = interest_payment
            
    
    @staticmethod
    def js_vars(player):
        return js_and_template_vars(player)
    
    @staticmethod
    def vars_for_template(player):
        return js_and_template_vars(player)

class FoodPriceEstimate6(Page):
    form_model = 'player'
    form_fields = ['food_price_estimate_6']
    template_name = 'savings_game_common/FoodPriceEstimate6.html'


    def is_displayed(player):
        return player.round_number == 6

class FoodPriceEstimate12(Page):
    form_model = 'player'
    form_fields = ['food_price_estimate_12']
    template_name = 'savings_game_common/FoodPriceEstimate12.html'


    def is_displayed(player):
        return player.round_number == 12


class Results(Page):
    template_name = 'savings_game_common/Results.html'

    def is_displayed(self):
        return self.round_number == C.NUM_ROUNDS
    
    def vars_for_template(player):
        total_interest_payments = 0
        total_asset_payments = 0
        total_salaries = 0
        total_food_expense = 0

        leftover_food = 0
        final_cash = 0
        
        player_in_final_round = player.in_round(C.NUM_ROUNDS)
        if not player_in_final_round.field_maybe_none('dead'):
            leftover_food = player.food
            final_cash = player.cash
        
        for p in player.in_all_rounds():
            total_interest_payments += p.interest_payment
            total_asset_payments += p.asset_payment
            total_salaries += p.salary
            total_food_expense += p.food_expense
            
            if p.round_number == player_in_final_round.field_maybe_none('death_round'):
                leftover_food = p.food
                final_cash = p.cash
            
        # set payoff if paid for real
        part = player.participant
        part.vars["game_payoff"] = final_cash
        if part.vars.get('pay_for_real', False) and part.vars.get('pay_round', None) == C.GAME_ROUND:
            player.payoff = final_cash * player.session.config['real_world_currency_per_point']
            
            
        return {
            'game_round': C.GAME_ROUND,
            'player_dead': player_in_final_round.dead,
            'final_cash': final_cash,
        }


page_sequence = [Savings, FoodPriceEstimate6, FoodPriceEstimate12, Results]
