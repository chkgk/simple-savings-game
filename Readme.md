# Simple savings game
Based on the [savings-game](https://github.com/o-nate/savings-game) by Nathaniel Lawrence.

## Explanation
Ahe app savings_game implements 12 rounds of a savings game. The player starts with a cash balance and a food stock. The player receives a salary every round and needs to consume one unit of food every round. The food must be purchased at a given price, but can be stockpiled for later rounds. Food prices increase with inflation. There are two inflation regimes which can be selected via session config variables. All variables can be set via constants. 

The player chooses how much food to purchase in each round and how much to invest in a risky asset, defined by an expected return and a volatility. Every round, one unit of food is consumed, the investment is played out, salaries are paid and interest is accrued on the remaining cash balance.

## To do:

- add questionnaires
- implement a training period
- implement two apps to have two rounds with different regiemes
- implement "death" that occurs if player does not have food left to consume and not enough cash to purchase more food
- calibrate parameters
- fix floating point result display

## Setup:
Clone the repository:
```bash
git clone https://github.com/chkgk/simple-savings-game.git
```

Initialize and activate a new virtual environment
```bash
python -m venv .venv

# windows
.\.venv\Scripts\activate

# mac / unix
.venv/bin/activate
```
Install the dependencies
```bash
pip install -r requirements.txt
```

Run oTree's devserver
```bash
otree devserver
```