from strats.custom_strats import MartingaleStrat

from stratchecker.stratchecker import Strat_checker

import logging

logging.basicConfig(level=logging.INFO)

#set logger format 



def main():
    strat = MartingaleStrat("Martingale",
                            start_balance=25,
                            base_bet=0.1,
                            max_bet=1,
                            multiplier=2,
                            max_bets=5 )
    print(strat.describe())

    strat_checker = Strat_checker(strat, "results1.txt")
    strat_checker.read_results()
    strat_checker.run()
    print(strat.balance)








if __name__ == "__main__":
    main()

