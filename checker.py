
from strats.custom_strats import MartingaleStrat, AntiMartingaleStrat, DAlembertStrat, ParoliStrat, one_3_2_6Strat,AntiDAlembertStrat,FibonacciStrat,DAlembertStopLossCooldownStrat
from stratchecker.stratchecker import Strat_checker
from strats.strats import Strat

import logging
from rich import print
import pickle
import os
import numpy as np

logging.basicConfig(format='%(message)s', level=logging.INFO, datefmt='%m/%d/%Y %I:%M:%S')





start_balance=1000
base_bet=0.1
max_bet=10
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

def save_slices(slices):
    with open('slices.pickle', 'wb') as f:
        pickle.dump(slices, f, pickle.HIGHEST_PROTOCOL)


def load_slices():
    with open('slices.pickle', 'rb') as f:
        return pickle.load(f)

def main():
    slices = []
    strats = []
    results = read_results("results.txt")


    #check if slices.pickle exists
    #if it does load it
    #if it does not create it
    if os.path.isfile('slices.pickle'):
        slices = load_slices()

    if slices[0][1] - slices[0][0] == max_bets and len(slices) == runs_per_strat:
        print("slices are correct")
    else:
        slices = Strat_checker.slice_results(count=runs_per_strat,max_bets=max_bets,results_length=len(results))
        # slices = Strat_checker.slice_results_with_overlap(count=runs_per_strat,max_bets=max_bets,results_length=len(results),overlap_percent=0.2)
        save_slices(slices)
        print("slices are incorrect, new slices created")
    
    
    
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
    

    strats.append(DAlembertStrat(description="DAlembertStrat",
                        start_balance=start_balance,
                        base_bet=base_bet,
                        max_bet=max_bet,
                        multiplier=multiplier,
                        max_bets=max_bets,
                        ))
    
    strats.append(AntiDAlembertStrat("AntiDAlembertStrat",
                        start_balance=start_balance,
                        base_bet=base_bet,
                        max_bet=max_bet,
                        multiplier=multiplier,
                        max_bets=max_bets ))
    

    strats.append(DAlembertStopLossCooldownStrat(description="DAlembertStopLossCooldownStrat",
                            start_balance=start_balance,
                            base_bet=base_bet,
                            max_bet=max_bet,
                            multiplier=multiplier,
                            max_bets=max_bets,
                            max_lose_streak = 5,
                            stop_loss_cooldown = 10
                            ))
    
    strats.append(FibonacciStrat("FibonacciStrat",
                            start_balance=start_balance,
                            base_bet=base_bet,
                            max_bet=5,
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
      
    


    


    
    strat_runners = []
    for strat in strats:
        strat_runners.append(Strat_checker(strat, results, slices=slices))
    

    for strat_runner in strat_runners:
        strat_runner.run(count=runs_per_strat,plot_graph=True)


    for strat_runner in strat_runners:
        strat_runner.report_as_string()

    for strat_runner in strat_runners:
        print(strat_runner.report())









if __name__ == "__main__":
    main()

