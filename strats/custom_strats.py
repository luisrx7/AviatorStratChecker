from strats.strats import Strat



class MartingaleStrat(Strat):

    def __init__(self,description,start_balance, base_bet, max_bet, multiplier ,max_bets=1000):
        super().__init__(description,start_balance, base_bet, max_bet, multiplier ,max_bets=1000)
        

    def on_win(self):
        super().on_win()

        self.bet = self.base_bet

    def on_lose(self):
        super().on_lose()
        
        self.bet = self.bet * 2


