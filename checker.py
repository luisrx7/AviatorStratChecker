
from strats.custom_strats import MartingaleStrat, AntiMartingaleStrat, DAlembertStrat, ParoliStrat, one_3_2_6Strat
from stratchecker.stratchecker import Strat_checker

import logging

logging.basicConfig(format='%(message)s', level=logging.ERROR, datefmt='%m/%d/%Y %I:%M:%S')


#set logger format 



start_balance=25
base_bet=0.1
max_bet=1
multiplier=2
max_bets=1000
runs_per_strat=5



def read_results(results_filename):
    #read file
    with open(results_filename) as f:
        file_content = f.readlines()

    #remove timestamp and newline
    results = [float(x.split(",")[1].replace("\n","")) for x in file_content]
    #invert list
    results.reverse()

    return results



def main():
    slices = []
    strats = []
    
    strats.append(MartingaleStrat("Martingale",
                            start_balance=start_balance,
                            base_bet=base_bet,
                            max_bet=max_bet,
                            multiplier=multiplier,
                            max_bets=max_bets ))
    
    
    strats.append(AntiMartingaleStrat("AntiMartingale",
                            start_balance=start_balance,
                            base_bet=base_bet,
                            max_bet=max_bet,
                            multiplier=multiplier,
                            max_bets=max_bets ))
    
    strats.append(DAlembertStrat("DAlembert",
                            start_balance=start_balance,
                            base_bet=base_bet,
                            max_bet=max_bet,
                            multiplier=multiplier,
                            max_bets=max_bets ))
    
    strats.append(ParoliStrat("Paroli",
                            start_balance=start_balance,
                            base_bet=base_bet,
                            max_bet=max_bet,
                            multiplier=multiplier,
                            max_bets=max_bets ))
    strats.append(one_3_2_6Strat("one_3_2_6",
                            start_balance=start_balance,
                            base_bet=base_bet,
                            max_bet=max_bet,
                            multiplier=multiplier,
                            max_bets=max_bets ))
      
    
    results = read_results("results.txt")
    slices = Strat_checker.slice_results(count=5,max_bets=max_bets,results_length=len(results))
    
    strat_runners = []
    for strat in strats:
        strat_runners.append(Strat_checker(strat, results, slices=slices))
    

    for strat_runner in strat_runners:
        strat_runner.run(count=runs_per_strat)
        


    for strat_runner in strat_runners:
        strat_runner.report()










if __name__ == "__main__":
    main()

