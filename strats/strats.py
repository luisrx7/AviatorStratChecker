

import logging
from strats.exceptions import MaxBetsReached, InsufficientFunds

logger = logging.getLogger(__name__)


class Strat():

    def __init__(self,description,start_balance, base_bet, max_bet, multiplier ,max_bets=1000):
        self.description = description
        self.start_balance = start_balance
        self.balance = start_balance
        self.base_bet = base_bet
        self.bet = base_bet
        self.max_bet = max_bet
        self.multiplier = multiplier
        self.initial_multiplier = multiplier
        self.win_streak = 0
        self.lose_streak = 0
        self.max_bets = max_bets
        self.number_of_bets = 0
        self.win_count = 0
        self.lose_count = 0
        


    def description(self):
        return self.description
    
    def describe(self):
        #return a string describing the strat and all of its parameters can be multiline
        return f"""{self.description}
        start balance: {self.start_balance}
        base bet: {self.base_bet}
        max bet: {self.max_bet}
        multiplier: {self.multiplier}
        max bets: {self.max_bets}
        """
    
    def get_balance(self):
        return self.balance

    def calculate_bet(self, result):
        '''
        result represents where the plane crashed
        if the plane crashed below the multiplier, it is a loss
        if the plane crashed above the multiplier, it is a win 
        '''

        logging.info(f"result: {result},  multiplier: {self.multiplier},  bet: {self.bet}, balance: {self.balance:.2f}, win streak: {self.win_streak}, lose streak: {self.lose_streak}")
        if self.multiplier < result:
            self.on_win()
        else:
            self.on_lose()

    def gamble(self):
        #take the bet from the balance
        logging.debug(f"\nbet {self.bet} - {self.multiplier}  from balance {self.balance:.2f}")

        if self.number_of_bets >= self.max_bets:
            logging.error(f"number of bets allowed {self.max_bets} reached, not betting anymore")
            self.bet = 0
            self.multiplier = 0
            raise MaxBetsReached
        if self.bet > self.balance:
            logging.info(f"bet {self.bet} is greater than balance {self.balance:.2f} cannot bet anymore")
            self.bet = 0
            self.multiplier = 0
            raise InsufficientFunds
        if self.bet > self.max_bet:
            logging.info(f"bet {self.bet} is greater than max bet {self.max_bet} using max bet {self.max_bet} instead")
            self.bet = self.max_bet
        
        self.multiplier = self.initial_multiplier
        self.balance = self.balance - self.bet
        self.number_of_bets += 1

        

    def on_win(self):
        #bet manipulation should be  implemented in subclass
        logging.info(f"win : previous bet: {self.bet}, previous balance: {self.balance:.2f}, new balance: {self.balance + self.bet * self.multiplier:.2f}")
        self.balance += self.bet * self.multiplier
        self.win_streak += 1
        self.lose_streak = 0
        self.win_count += 1

    def on_lose(self):
        #bet manipulation should be  implemented in subclass
        logging.warn(f"lose : previous bet: {self.bet}, previous balance: {self.balance:.2f}, new balance: {self.balance - self.bet:.2f}")
        self.win_streak = 0
        self.lose_streak += 1
        self.lose_count += 1


    def reset(self):

        logging.info(f"game start : base bet: {self.bet}, balance: {self.balance:.2f}")
        self.bet = self.base_bet
        self.win_streak = 0
        self.lose_streak = 0
        self.number_of_bets = 0
        self.multiplier = self.initial_multiplier
        self.win_count = 0
        self.lose_count = 0
        self.balance = self.start_balance
        
            
    def report(self):
        # print the  final balance
        return(f"""\nResume:
        start balance: {self.start_balance}
        final balance: {self.balance:.2f}
        won: {self.balance - self.start_balance:.2f}
        win count: {self.win_count}
        lose count: {self.lose_count}
        bet count: {self.number_of_bets}
        """)




