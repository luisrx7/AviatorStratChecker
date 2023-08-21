import unittest
from strats.strats import Strat  

class TestStrat(unittest.TestCase):

    def setUp(self):
        self.strat = Strat("Test Strat", 1000, 10, 200, 1.5, 100)

    def test_init(self):
        self.assertEqual(self.strat.description, "Test Strat")
        self.assertEqual(self.strat.start_balance, 1000)
        self.assertEqual(self.strat.bet, 10)

    def test_calculate_bet_win(self):
        self.strat.calculate_bet(1.7) # 1.7 > 1.5. So, it is a win.
        self.assertEqual(self.strat.win_streak, 1)
        self.assertEqual(self.strat.lose_streak, 0)

    def test_calculate_bet_lose(self):
        self.strat.calculate_bet(1.3) # 1.3 < 1.5. So, it is a lose.
        self.assertEqual(self.strat.win_streak, 0)
        self.assertEqual(self.strat.lose_streak, 1)

    def test_on_win(self):
        self.strat.gamble() # take the bet from the balance 1000 - 10 = 990
        self.strat.on_win() 
        self.assertEqual(self.strat.balance, 1005.0) # 990 + (10 * 1.5) = 1005 
        self.assertEqual(self.strat.win_streak, 1)

    def test_on_lose(self):
        self.strat.gamble()
        self.strat.on_lose()
        self.assertEqual(self.strat.balance, 990.0)  # 1000 - 10 = 990
        self.assertEqual(self.strat.lose_count, 1)

    def test_reset(self):
        # change the state
        self.strat.calculate_bet(1.3)
        self.strat.on_lose()
        # state is reset
        self.strat.reset()
        self.assertEqual(self.strat.win_streak, 0)
        self.assertEqual(self.strat.lose_streak, 0)
        self.assertEqual(self.strat.number_of_bets, 0)
        self.assertEqual(self.strat.balance, self.strat.start_balance)

    def test_report(self):
        report = self.strat.report()
        self.assertIn("start balance: 1000", report)
        self.assertIn("final balance: 1000.0", report)
        self.assertIn("won: 0.0", report)
        self.assertIn("bet count: 0", report)

if __name__ == '__main__':
    unittest.main()