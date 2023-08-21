from strats.strats import Strat
from strats.exceptions import MaxBetsReached, InsufficientFunds

import logging

import random
from rich import print

logger = logging.getLogger(__name__)



class Strat_checker():
    def __init__(self, strat:Strat, results, slices=[]) -> None:
        self.strat = strat
        self.slices = slices
        self.strat_reports = []
        self.results = results


    

    @staticmethod
    def slice_results(count,max_bets,results_length):
        
        '''
        slice results in a random place making sure that
        the max_length of the slice is not exceeded
        return the slice indexes

        #TODO
        a good slice is one that contains a loss streak of at least 6 losses assuming a
        multiplier of 2
        based on the assumption that the strat will recover from that loss streak

        '''
        slices = []
        for i in range(count):
            #get random start index
            start_index = random.randint(0,results_length-max_bets)
            
            #get random end index
            end_index = start_index+max_bets
                        
            slices.append((start_index,end_index))
        
        return slices
    
        
        
    
    
    

    def report(self):
        print(f"\nStrategy: {self.strat.description}")
        for report in self.strat_reports:
            print(report)            

    
    def get_slices(self):
        return self.slices
    
    def set_slices(self,slices):
        self.slices = slices
    

    def run(self,count:int=1,random_slice:bool=True):
        '''
        run the strat count times
        if random_slice is True, slice the results in a random places 
        count must be greater than 1 if random_slice is True
        '''
        

        
        if random_slice is True and count == 1:
            logging.warning("random_slice is True and count is 1, setting random_slice to False")
            random_slice = False
        
        if self.strat.max_bets > len(self.results):
            logging.warning(f"max bets {self.strat.max_bets} is greater than the number of results {len(self.results)}, setting max bets to {len(self.results)}")
            self.strat.max_bets = len(self.results)
        
        
        if len(self.slices) == 0:
            #if no slices are defined, generate count slices
            self.slices = self.slice_results(self.strat.max_bets,count)
        
            
        for i in range(count):

            self.strat.reset()
            try:
                for result in self.results[self.slices[i][0]:self.slices[i][1]]:
                    self.strat.gamble()
                    self.strat.calculate_bet(result)
                    
            except MaxBetsReached or InsufficientFunds:
                pass
            
            except Exception as e:
                logging.error(e)
            
            finally:
                self.strat_reports.append(self.strat.report_as_string() + f"slice: {self.slices[i]}")
                

                




    