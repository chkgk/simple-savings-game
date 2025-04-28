from otree.api import *

# Models
class C(BaseConstants):
    NAME_IN_URL = 'post_survey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    risk_choice = models.IntegerField(
        label="Which gamble do you choose?",
        choices=[
            (1, '16,16'),
            (2, '24,12'),
            (3, '32,8'),
            (4, '40,4'),
            (5, '48,0'),
        ],
        widget=widgets.RadioSelect,
    )

    finlit_q1 = models.StringField(
        label="Suppose you had €100 in a savings account, and the interest rate is 2% per year. How much money would you have in the account after 5 years if you leave it untouched?",
        choices=[
            ('more_102', 'More than €102'),
            ('exact_102', 'Exactly €102'),
            ('less_102', 'Less than €102'),
            ('dont_know', 'Don’t know'),
        ],
        widget=widgets.RadioSelect,
    )

    finlit_q2 = models.StringField(
        label="Imagine the interest rate on your savings account is 1% per year, and inflation is 2% per year. After one year, how much could you buy with the money in this account?",
        choices=[
            ('more', 'More than today'),
            ('same', 'Exactly the same as today'),
            ('less', 'Less than today'),
            ('dont_know', 'Don’t know'),
        ],
        widget=widgets.RadioSelect,
    )

    finlit_q3 = models.StringField(
        label='Please tell me whether this statement is true or false: “Buying a single company’s stock is usually safer than investing in a stock mutual fund.”',
        choices=[
            ('true', 'True'),
            ('false', 'False'),
            ('dont_know', 'Don’t know'),
        ],
        widget=widgets.RadioSelect,
    )

    time_preference_1 = models.StringField(choices=[('A', 'Today'), ('B', 'In 6 Months')], widget=widgets.RadioSelect)
    time_preference_2 = models.StringField(choices=[('A', 'Today'), ('B', 'In 6 Months')], widget=widgets.RadioSelect)
    time_preference_3 = models.StringField(choices=[('A', 'Today'), ('B', 'In 6 Months')], widget=widgets.RadioSelect)
    time_preference_4 = models.StringField(choices=[('A', 'Today'), ('B', 'In 6 Months')], widget=widgets.RadioSelect)
    time_preference_5 = models.StringField(choices=[('A', 'Today'), ('B', 'In 6 Months')], widget=widgets.RadioSelect)
    time_preference_6 = models.StringField(choices=[('A', 'Today'), ('B', 'In 6 Months')], widget=widgets.RadioSelect)

    compound_q1 = models.StringField(
        label="If inflation is 10% a year, and a product currently costs 1000 €, how much will it cost in one year’s time?")

    compound_q2 = models.StringField(
        label="If inflation is 50% a year, and a product currently costs 1000 €, how much will it cost in two years’ time?",
        choices=[
            ('less_2000', 'Less than 2000 €'),
            ('more_2000', 'More than 2000 €'),
            ('exact_2000', '2000 €'),
        ],
        widget=widgets.RadioSelect,
    )

    compound_q3 = models.StringField(
        label="If inflation is 3% a year, and a product currently costs 1000 €, how much will it cost in five years’ time?",
        choices=[
            ('more_1150', 'More than 1150 €'),
            ('exact_1150', '1150 €'),
            ('less_1150', 'Less than 1150 €'),
        ],
        widget=widgets.RadioSelect,
    )

    compound_q4 = models.StringField(
        label="If inflation is 100% a year, and a product currently costs 1000 €, how much will it cost in five years’ time?")

    age = models.IntegerField(label="How old are you?", min=10, max=120)

    gender = models.StringField(
        label="What’s your gender?",
        choices=[
            ('female', 'Female'),
            ('male', 'Male'),
            ('diverse', 'Diverse'),
            ('no_answer', 'Prefer not to say'),
        ],
        widget=widgets.RadioSelect,
    )

    education = models.StringField(
        label="What is the highest level of education you have completed?",
        choices=[
            ('none', 'No formal education'),
            ('school', 'Compulsory schooling (e.g., Hauptschule, Neue Mittelschule)'),
            ('apprenticeship', 'Apprenticeship (Lehre)'),
            ('matura', 'Matura, Abitur, etc. (e.g., HTL, HAK)'),
            ('bachelor', 'Bachelor’s degree'),
            ('master', 'Master’s degree'),
            ('doctorate', 'Doctorate'),
        ],
        widget=widgets.RadioSelect,
    )

    investment_experience = models.StringField(
        label="How would you describe your experience with investments?",
        choices=[
            ('very_exp', 'Very experienced'),
            ('somewhat_exp', 'Somewhat experienced'),
            ('little_exp', 'Little experience'),
            ('no_exp', 'No experience'),
        ],
        widget=widgets.RadioSelect,
    )


# Pages
class Page1(Page):
    form_model = 'player'
    form_fields = ['risk_choice']

    def vars_for_template(player):
        return {
            'gambles': [
                {'value': 1, 'event_a': '16', 'event_b': '16'},
                {'value': 2, 'event_a': '24', 'event_b': '12'},
                {'value': 3, 'event_a': '32', 'event_b': '8'},
                {'value': 4, 'event_a': '40', 'event_b': '4'},
                {'value': 5, 'event_a': '48', 'event_b': '0'},
            ]
        }

class Page2(Page):
    form_model = 'player'
    form_fields = ['finlit_q1', 'finlit_q2', 'finlit_q3']

class Page3(Page):
    form_model = 'player'
    form_fields = [
        'time_preference_1',
        'time_preference_2',
        'time_preference_3',
        'time_preference_4',
        'time_preference_5',
        'time_preference_6',
    ]

    def vars_for_template(player):
        return {
            'rows': [{'index': i, 'today': 10, 'future': 10 + i} for i in range(1, 7)]
        }

class Page4(Page):
    form_model = 'player'
    form_fields = ['compound_q1', 'compound_q2', 'compound_q3', 'compound_q4']

class Page5(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'education', 'investment_experience']

class Summary(Page):
    def vars_for_template(player):
        return {"pay_for_real": player.participant.vars.get('pay_for_real', False)}


page_sequence = [Page1, Page2, Page3, Page4, Page5, Summary]