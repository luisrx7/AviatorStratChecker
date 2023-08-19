from strats.strats import Strat



class MartingaleStrat(Strat):

    def __init__(self,description,start_balance, base_bet, max_bet, multiplier ,max_bets):
        super().__init__(description,start_balance, base_bet, max_bet, multiplier ,max_bets)
        

    def on_win(self):
        super().on_win()

        self.bet = self.base_bet

    def on_lose(self):
        super().on_lose()
        
        self.bet = self.bet * 2


class AntiMartingaleStrat(Strat):
    '''
    Reverse Martingale
    One compelling alternative is the Reverse Martingale, also known as 
    the Anti-Martingale. As opposed to doubling your bet amount after a
    loss at online casinos, the Reverse Martingale instructs you to 
    double your bet amount after a win. When you lose, you go back to 
    the start and bet 1 unit again.

    This system is designed to capitalize on winning streaks. However, 
    all of your previous profits can be wiped out with a single loss, 
    so this system is best used in short bursts.
    '''
    
    def __init__(self,description,start_balance, base_bet, max_bet, multiplier ,max_bets):
        super().__init__(description,start_balance, base_bet, max_bet, multiplier ,max_bets)
    
    def on_win(self):
        super().on_win()

        self.bet = self.bet * 2

    def on_lose(self):
        super().on_lose()
        
        self.bet = self.base_bet
        