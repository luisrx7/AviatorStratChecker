from strats.custom_strats import MartingaleStrat, AntiMartingaleStrat

from stratchecker.stratchecker import Strat_checker

import logging

logging.basicConfig(format='%(message)s', level=logging.INFO, datefmt='%m/%d/%Y %I:%M:%S')


#set logger format 



def main():
    slices = []
    
    strat = MartingaleStrat("Martingale",
                            start_balance=25,
                            base_bet=0.1,
                            max_bet=1,
                            multiplier=2,
                            max_bets=1000 )
    print(strat.describe())
    
    
    strat2 = AntiMartingaleStrat("AntiMartingale",
                            start_balance=25,
                            base_bet=0.1,
                            max_bet=1,
                            multiplier=2,
                            max_bets=1000 )
    

    
    strat_checker = Strat_checker(strat, "results.txt")
    strat_checker.read_results()
    strat_checker.run(count=5,random_slice=True)
    slices = strat_checker.get_slices()
    
    strat_checker2 = Strat_checker(strat2, "results.txt")
    strat_checker2.read_results()
    strat_checker2.set_slices(slices)
    strat_checker2.run(count=5,random_slice=False)
     
    
    strat_checker.report()
    
    strat_checker2.report()
    
    print(strat.balance)








if __name__ == "__main__":
    main()

