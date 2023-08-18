import unittest
from unittest.mock import patch
from strats import Strat

class TestStrat(unittest.TestCase):

    def setUp(self):
        self.start_balance = 1000
        self.base_bet = 10
        self.max_bet = 100
        self.multiplier = 2
        self.max_bets = 5
        self.strat = Strat("Test Strategy", self.start_balance, self.base_bet, self.max_bet, self.multiplier, self.max_bets)

    def test_init(self):
        self.assertEqual(self.strat.description, "Test Strategy")
        self.assertEqual(self.strat.start_balance, self.start_balance)
        self.assertEqual(self.strat.balance, self.start_balance)
        self.assertEqual(self.strat.base_bet, self.base_bet)
        self.assertEqual(self.strat.bet, self.base_bet)
        self.assertEqual(self.strat.max_bet, self.max_bet)
        self.assertEqual(self.strat.multiplier, self.multiplier)
        self.assertEqual(self.strat.win_streak, 0)
        self.assertEqual(self.strat.lose_streak, 0)
        self.assertEqual(self.strat.max_bets, self.max_bets)
        self.assertEqual(self.strat.number_of_bets, 0)

    @patch('logging.info')
    def test_gamble(self, mock_logging_info):
        self.strat.bet = 50
        self.strat.gamble()

        self.assertEqual(self.strat.balance, self.start_balance - self.strat.bet)
        self.assertEqual(self.strat.number_of_bets, 1)
        mock_logging_info.assert_called_with(f"bet {self.strat.bet} - {self.strat.multiplier}  from balance {self.start_balance:.2f}")


    @patch('logging.info')
    def test_gamble_max_bets_reached(self, mock_logging_info):
        self.strat.number_of_bets = self.max_bets
        self.strat.gamble()

        self.assertEqual(self.strat.balance, self.start_balance)
        mock_logging_info.assert_called_with(f"number of bets allowed {self.max_bets} reached, not gamble anymore")

    @patch('logging.info')
    def test_gamble_insufficient_balance(self, mock_logging_info):
        self.strat.bet = self.start_balance + 1
        self.strat.gamble()

        self.assertEqual(self.strat.balance, self.start_balance)
        mock_logging_info.assert_called_with(f"bet 1001 is greater than balance {self.start_balance:.2f} cannot gamble anymore")

    @patch.object(Strat, 'on_win')
    def test_calculate_bet_win(self, mock_on_win):
        result = self.multiplier + 1
        self.strat.calculate_bet(result)
        mock_on_win.assert_called_once()

    @patch.object(Strat, 'on_lose')
    def test_calculate_bet_lose(self, mock_on_lose):
        result = self.multiplier - 1
        self.strat.calculate_bet(result)
        mock_on_lose.assert_called_once()

if __name__ == '__main__':
    unittest.main()
