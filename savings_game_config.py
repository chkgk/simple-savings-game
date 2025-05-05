SAVINGS_GAME_CONFIG = {
    'low': {
        'INITIAL_CASH': 30,
        'INITIAL_FOOD': 0,
        'INITIAL_SALARY': 8.00,
        'INITIAL_FOOD_PRICE': 4.20,
        'SAVINGS_INTEREST_RATE': 0.019,
        'ASSET_PAYOFFS': [1.6, 0.75, 1.6, 1.6, 0.75, 1.6, 0.75, 1.6, 1.6, 0.75, 0.75, 0.75],
        'INFLATION_RATE': 0.05
    },
    'high': {
        'INITIAL_CASH': 30,
        'INITIAL_FOOD': 0,
        'INITIAL_SALARY': 8.00,
        'INITIAL_FOOD_PRICE': 4.20,
        'SAVINGS_INTEREST_RATE': 0.019,
        'ASSET_PAYOFFS': [1.6, 0.75, 1.6, 1.6, 0.75, 1.6, 0.75, 1.6, 1.6, 0.75, 0.75, 0.75],
        'INFLATION_RATE': 0.15
    },
    'training': {
        'INITIAL_CASH': 30,
        'INITIAL_FOOD': 0,
        'INITIAL_SALARY': 8.00,
        'INITIAL_FOOD_PRICE': 4.20,
        'SAVINGS_INTEREST_RATE': 0.019,
        'ASSET_PAYOFFS': [1.6, 0.75, 1.6, 1.6, 0.75, 1.6, 0.75, 1.6, 1.6, 0.75, 0.75, 0.75],
        'INFLATION_RATE': 0.0
    }
}

TEST_PURCHASE_PLAN = [
    {'food_purchase': 1, 'risky_investment': 1}
    for _ in range(12)
]

TEST_FINAL_CASH_AMOUNTS = {
    'low': [
            30.00,
            34.87,
            38.77,
            43.37,
            47.82,
            51.26,
            55.35,
            58.4,
            62.07,
            65.5,
            67.84,
            69.89,
            71.61
    ],
    'high': [
            30.00,
            34.87,
            38.34,
            41.99,
            44.86,
            45.96,
            46.81,
            45.53,
            43.59,
            39.91,
            33.34,
            24.39,
            12.56
    ]
}