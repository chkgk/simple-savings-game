from otree.api import *
from savings_game_config import SAVINGS_GAME_CONFIG
import random

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'savings_game'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 12 + 1  # last one is not actually played, we just need it for calculations
    PAYMENT_PROBABILITY = 0.1
    

class Subsession(BaseSubsession):
    initial_cash = models.CurrencyField()
    initial_food = models.IntegerField()
    initial_salary = models.CurrencyField()
    initial_food_price = models.CurrencyField()
    savings_interest_rate = models.FloatField()
    asset_expected_return = models.FloatField()
    asset_standard_deviation = models.FloatField()
    inflation_rate = models.FloatField()
    inflation_regime = models.StringField()


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    food_purchase = models.IntegerField()
    risky_investment = models.CurrencyField()
    
    dead = models.BooleanField(default=False)
    death_round = models.IntegerField()
    death_reason = models.StringField()
    
    cash = models.CurrencyField()
    food = models.IntegerField()
    
    salary = models.CurrencyField(default=0)
    food_expense = models.CurrencyField(default=0)
    interest_payment = models.CurrencyField(default=0)
    asset_payment = models.CurrencyField(default=0)
    realized_asset_payoff = models.FloatField(blank=True)

    food_price_estimate_6 = models.StringField(label="Estimation (after 6 months)")
    food_price_estimate_12 = models.StringField(label="Estimation (after 12 months)")
    
# FUNCTIONS

def creating_session(subsession):
    regime = subsession.session.config['inflation_regime']
    config = SAVINGS_GAME_CONFIG[regime]
    
    subsession.inflation_regime = regime
    subsession.initial_cash = config['INITIAL_CASH']
    subsession.initial_food = config['INITIAL_FOOD']
    subsession.initial_salary = config['INITIAL_SALARY']
    subsession.initial_food_price = config['INITIAL_FOOD_PRICE']
    subsession.savings_interest_rate = config['SAVINGS_INTEREST_RATE']
    # subsession.asset_expected_return = config['ASSET_EXPECTED_RETURN']
    # subsession.asset_standard_deviation = config['ASSET_STANDARD_DEVIATION']
    subsession.inflation_rate = config['INFLATION_RATE']
    
    for p in subsession.get_players():
        if p.round_number == 1:
            p.cash = subsession.initial_cash
            p.food = subsession.initial_food
            p.participant.vars["pay_for_real"] = random.random() <= C.PAYMENT_PROBABILITY

def get_food_price(player):
    subs = player.subsession
    if player.round_number == 1:
        return subs.initial_food_price
    return subs.initial_food_price * (1 + subs.inflation_rate) ** (player.round_number - 1)

def js_and_template_vars(player):
    subs = player.subsession
    return {
        'food_price': cu(get_food_price(player)),
        'cash': player.cash,
        'food': player.food,
        'salary': cu(subs.initial_salary),
        'interest_rate': subs.savings_interest_rate * 100,
        # 'asset_expected_return': subs.asset_expected_return * 100,
        'max_rounds': C.NUM_ROUNDS - 1,
        'realized_asset_payoff': player.field_maybe_none("realized_asset_payoff") or '-',
    }

def get_asset_payment_uniform(subsession, investment):
    mu = subsession.asset_expected_return
    sigma = subsession.asset_standard_deviation
    sample = random.gauss(mu, sigma)
    return investment * sample

def get_asset_payment(subsession, investment):
    regime = subsession.session.config['inflation_regime']
    payoff_list = SAVINGS_GAME_CONFIG[regime]['ASSET_PAYOFFS']
    realized_payoff = payoff_list[subsession.round_number - 1]
    return realized_payoff, realized_payoff * investment

# PAGES
class Savings(Page):
    form_model = 'player'
    form_fields = ['food_purchase', 'risky_investment']
    
    def is_displayed(player):
        # do not play the last round, just use if for calculations
        # make sure to skip if player is dead
        return player.round_number < C.NUM_ROUNDS and not player.in_round(C.NUM_ROUNDS).dead
    
    def before_next_page(player, timeout_happened):
        subs = player.subsession
        
        current_cash = player.cash
        food_price = get_food_price(player)
        food_expense = player.food_purchase * food_price
        asset_expense = player.risky_investment
        unspent_cash = current_cash - food_expense - asset_expense
        player.food_expense = food_expense
        
        # calculate new food
        new_food = player.food - 1 + player.food_purchase
        
        
        # calculate new cash
        interest_payment = cu(unspent_cash * subs.savings_interest_rate)
        asset_realization, asset_payoff = get_asset_payment(subs, player.risky_investment)
        asset_payment = cu(asset_payoff)
        salary = subs.initial_salary
        new_cash = unspent_cash + salary + interest_payment + asset_payment + asset_expense
        
        # new food price
        new_food_price = food_price * (1 + subs.inflation_rate)
        
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

    def is_displayed(player):
        return player.round_number == 6

class FoodPriceEstimate12(Page):
    form_model = 'player'
    form_fields = ['food_price_estimate_12']

    def is_displayed(player):
        return player.round_number == 12


class Results(Page):
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
        if player.participant.vars.get('pay_for_real', False):
            player.payoff = final_cash
            
        return {
            'total_interest_payments': total_interest_payments,
            'total_asset_payments': total_asset_payments,
            'total_salaries': total_salaries,
            'total_food_expense': total_food_expense,
            'leftover_food': leftover_food,
            'final_cash': final_cash,
            'player_dead': player_in_final_round.dead,
            'player_death_round': player_in_final_round.field_maybe_none('death_round'),
            'player_death_reason': player_in_final_round.field_maybe_none('death_reason'),
        }


page_sequence = [Savings, FoodPriceEstimate6, FoodPriceEstimate12, Results]
