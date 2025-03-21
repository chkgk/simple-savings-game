# Simple savings game
Based on the [savings-game](https://github.com/o-nate/savings-game) by Nathaniel Lawrence.

## Explanation
The app savings_game implements 12 rounds of a savings game. The player starts with a cash balance and a food stock. The player receives a salary every round and needs to consume one unit of food every round. The food must be purchased at a given price, but can be stockpiled for later rounds. Food prices increase with inflation. There are two inflation regimes which can be selected via session config variables. All variables can be set via constants. 

The player chooses how much food to purchase in each round and how much to invest in a risky asset, defined by an expected return and a volatility. Every round, one unit of food is consumed, the investment is played out, salaries are paid and interest is accrued on the remaining cash balance.

## To do:

- calibrate parameters

## Setup:
```bash
# Clone the repository:
git clone https://github.com/chkgk/simple-savings-game.git

# create a virtual environment
python -m venv .venv

# activate the environment
# windows
.\.venv\Scripts\activate

# mac / unix
.venv/bin/activate

# install the dependencies
pip install -r requirements.txt
```

Running the app
```bash
# activate the environment, if not already active
# windows
.\.venv\Scripts\activate

# mac / unix
.venv/bin/activate

# run oTree's devserver
otree devserver
```