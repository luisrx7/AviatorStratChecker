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
        

class DAlembertStrat(Strat):
    '''
    D Alembert System | Increase your bet amount by 1 unit whenever you lose and decrease by 1 unit if you win.
    1 unit = base_bet
    '''
    def __init__(self,description,start_balance, base_bet, max_bet, multiplier ,max_bets):
        super().__init__(description,start_balance, base_bet, max_bet, multiplier ,max_bets)
        if description == "":
            self.description = f"DAlembert"

    def on_win(self):
        super().on_win()
        if self.bet > self.base_bet:
            self.bet = round(self.bet - self.base_bet,2)
        else:
            self.bet = self.base_bet

    def on_lose(self):
        super().on_lose()
        
        if self.bet < self.max_bet:
            self.bet = round(self.bet + self.base_bet,2)
        else:
            self.bet = self.max_bet


class AntiDAlembertStrat(Strat):
    '''
    Anti D Alembert System | Increase your bet amount by 1 unit whenever you win and decrease by 1 unit if you lose.
    1 unit = base_bet
    '''
    def __init__(self,description,start_balance, base_bet, max_bet, multiplier ,max_bets):
        super().__init__(description,start_balance, base_bet, max_bet, multiplier ,max_bets)
        if description == "":
            self.description = f"DAlembert"

    def on_lose(self):
        super().on_lose()
        if self.bet > self.base_bet:
            self.bet = round(self.bet - self.base_bet,2)
        else:
            self.bet = self.base_bet


        
    def on_win(self):
        super().on_win()    

        if self.bet < self.max_bet:
            self.bet = round(self.bet + self.base_bet,2)
        else:
            self.bet = self.max_bet

class DAlembertStopLossCooldownStrat(Strat):
    '''
    D Alembert System | Increase your bet amount by 1 unit whenever you lose and decrease by 1 unit if you win.
    if you lose x times in a row, enter a cooldown period of y bets
    1 unit = base_bet
    '''
    def __init__(self,description,start_balance, base_bet, max_bet, multiplier ,max_bets, max_lose_streak, stop_loss_cooldown):
        super().__init__(description,start_balance, base_bet, max_bet, multiplier ,max_bets)
        if description == "":
            self.description = f"DAlembert Stop Loss Cooldown {max_lose_streak} {stop_loss_cooldown}"
        
        self.max_lose_streak = max_lose_streak
        self.stop_loss_cooldown = stop_loss_cooldown


    def on_win(self):
        super().on_win()    

        if self.bet < self.max_bet:
            self.bet = round(self.bet + self.base_bet,2)
        else:
            self.bet = self.max_bet

    def on_lose(self):
        super().on_lose()

        if self.lose_streak >= self.max_lose_streak:
            self.bet_cooldown = self.stop_loss_cooldown
        
        else:
            if self.bet > self.base_bet:
                self.bet = round(self.bet - self.base_bet,2)
            else:
                self.bet = self.base_bet


        




class ParoliStrat(Strat):
    '''
    Paroli System | Increase your bet amount by 1 unit whenever you win. If you win three times in a row, go back to the start and bet 1 unit again.    1 unit = base_bet
    '''
    def __init__(self,description,start_balance, base_bet, max_bet, multiplier ,max_bets):
        super().__init__(description,start_balance, base_bet, max_bet, multiplier ,max_bets)
        
        
    def on_win(self):
        super().on_win()

        if self.win_streak == 3:
            self.bet = self.base_bet
        else:
            self.bet = self.bet + self.base_bet

    def on_lose(self):
        super().on_lose()
        
        self.bet = self.base_bet

class OscarGrindStrat(Strat):
    '''
    Oscar Grind | Increase your bet amount by 1 unit after each win. Keep it the same when you lose. When you end up with at least 1 unit of profit, go back to the start and bet 1 unit again.    
    1 unit = base_bet

    needs work
    '''
    
    def __init__(self,description,start_balance, base_bet, max_bet, multiplier ,max_bets):
        super().__init__(description,start_balance, base_bet, max_bet, multiplier ,max_bets)
        
        
    def on_win(self):
        super().on_win()

        self.bet = self.bet + self.base_bet

    def on_lose(self):
        super().on_lose()
        
        self.bet = self.base_bet

class FibonacciStrat(Strat):
    '''
    Fibonacci | Increase your bet amount by the sum of the previous two bets after each loss. When you win, go back two numbers in the sequence and bet that amount.    
    1 unit = base_bet   

    needs work

    '''

    
    def __init__(self,description,start_balance, base_bet, max_bet, multiplier ,max_bets):
        super().__init__(description,start_balance, base_bet, max_bet, multiplier ,max_bets)
        self.fibonacci_sequence = [1,1,2,3,5,8,13,21,34,55,89,144,233,377,610]
        self.current_fibonacci_index = 0
        
    def on_win(self):
        super().on_win()
        #go down the fibonacci sequence by 2
        self.current_fibonacci_index -= 2 if self.current_fibonacci_index >= 2 else 0
        self.bet = self.bet + self.base_bet

    def on_lose(self):
        super().on_lose()
        #go up the fibonacci sequence
        self.current_fibonacci_index += 1 if self.current_fibonacci_index < len(self.fibonacci_sequence) else len(self.fibonacci_sequence)
        self.bet = self.base_bet * self.fibonacci_sequence[self.current_fibonacci_index]


class one_3_2_6Strat(Strat):
    '''
    1-3-2-6 System | Start by betting 1 unit, followed by 3 units, 2 units, and 6 units, before starting again, but only move up the sequence when you win.
    1 unit = base_bet

    not sure if this is implemented correctly
    '''
    
    def __init__(self,description,start_balance, base_bet, max_bet, multiplier ,max_bets):
        super().__init__(description,start_balance, base_bet, max_bet, multiplier ,max_bets)
        self.bet_sequence = [1,3,2,6]       
        
    def on_win(self):
        super().on_win()
        self.bet = self.bet_sequence[self.win_streak % len(self.bet_sequence)] * self.base_bet

    def on_lose(self):
        super().on_lose()
        
        self.bet = self.base_bet