import unittest
from strats.custom_strats import MartingaleStrat 
from strats.exceptions import MaxBetsReached, InsufficientFunds

class TestMartingaleStrat(unittest.TestCase):
    def setUp(self):
        self.start_balance = 1000
        self.base_bet = 10
        self.max_bet = 100
        self.multiplier = 2
        self.max_bets = 100
        self.strat = MartingaleStrat(
            "Martingale Strategy",
            self.start_balance,
            self.base_bet,
            self.max_bet,
            self.multiplier,
            self.max_bets
        )

    def test_initial_values(self):
        self.assertEqual(self.strat.start_balance, self.start_balance)
        self.assertEqual(self.strat.balance, self.start_balance)
        self.assertEqual(self.strat.base_bet, self.base_bet)
        self.assertEqual(self.strat.bet, self.base_bet)
        self.assertEqual(self.strat.max_bet, self.max_bet)
        self.assertEqual(self.strat.multiplier, self.multiplier)
        self.assertEqual(self.strat.initial_multiplier, self.multiplier)
        self.assertEqual(self.strat.win_streak, 0)
        self.assertEqual(self.strat.lose_streak, 0)
        self.assertEqual(self.strat.max_bets, self.max_bets)
        self.assertEqual(self.strat.number_of_bets, 0)
        self.assertEqual(self.strat.win_count, 0)
        self.assertEqual(self.strat.lose_count, 0)

    def test_on_win(self):
        self.strat.balance = 1000  # Simulating a win
        initial_bet = self.strat.bet
        initial_balance = self.strat.balance
        self.strat.gamble() # take the bet from the balance 1000 - 10 = 990
        self.strat.on_win()
        self.assertEqual(self.strat.balance, (initial_balance - self.strat.bet) + initial_bet * self.multiplier)
        self.assertEqual(self.strat.bet, self.base_bet)
        self.assertEqual(self.strat.win_streak, 1)
        self.assertEqual(self.strat.lose_streak, 0)
        self.assertEqual(self.strat.win_count, 1)
        self.assertEqual(self.strat.lose_count, 0)

    def test_on_lose(self):
        self.strat.balance = 900  # Simulating a loss
        initial_bet = self.strat.bet
        initial_balance = self.strat.balance
        self.strat.gamble() # take the bet from the balance 1000 - 10 (base_bet) = 990
        self.strat.on_lose()
        self.assertEqual(self.strat.balance, initial_balance - initial_bet)
        self.assertEqual(self.strat.bet, initial_bet * 2)
        self.assertEqual(self.strat.win_streak, 0)
        self.assertEqual(self.strat.lose_streak, 1)
        self.assertEqual(self.strat.win_count, 0)
        self.assertEqual(self.strat.lose_count, 1)

    # Add more tests for other methods as needed

if __name__ == '__main__':
    unittest.main()
