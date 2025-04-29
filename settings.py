from os import environ

SESSION_CONFIGS = [
    dict(
        name='instructions',
        display_name='Instructions',
        num_demo_participants=1,
        app_sequence=['instructions'],
        inflation_regime='training',
    ),
    dict(
        display_name='Savings game, 12 months, low inflation',
        name='savings_game_low',
        app_sequence=['savings_game_1'],
        num_demo_participants=2,
    ),
    dict(
        display_name='Savings game, 12 months, high inflation',
        name='savings_game_high',
        app_sequence=['savings_game_1'],
        num_demo_participants=2,
    ),
    dict(
        name='post_survey',
        display_name="Post-Experiment Survey",
        app_sequence=['post_survey'],
        num_demo_participants=1,
    ),
    dict(
        name='complete_experiment',
        display_name="Complete Experiment",
        app_sequence=['instructions', 'savings_game_1', 'savings_game_2', 'post_survey'],
        num_demo_participants=1,
        inflation_regime='high'
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0.10, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = ['treatment', 'pay_for_real', 'game_payoff', 'pay_round']
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'EUR'
USE_POINTS = False

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '4147388604890'

PAYMENT_URL = environ.get('PAYMENT_URL', '#')