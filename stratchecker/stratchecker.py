from strats.strats import Strat
from strats.exceptions import MaxBetsReached, InsufficientFunds

import logging

import random

logger = logging.getLogger(__name__)



class Strat_checker():
    def __init__(self, strat:Strat, results_filename:str, slices=[]) -> None:
        self.strat = strat
        self.results_filename = results_filename
        self.slices = slices

    
    def read_results(self):
        #read file
        with open(self.results_filename) as f:
            file_content = f.readlines()

        #remove timestamp and newline
        self.results = [float(x.split(",")[1].replace("\n","")) for x in file_content]
        #invert list
        self.results.reverse()


    def slice_results(self,max_length,count):
        
        '''
        slice results in a random place making sure that
        the max_length of the slice is not exceeded
        return the slice
        '''
        slices = []
        for i in range(count):
            #get random start index
            start_index = random.randint(0,len(self.results)-max_length)
            
            #get random end index
            end_index = start_index+max_length
                        
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
        self.strat_reports = []
        
        
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
                self.strat_reports.append(self.strat.report() + f"slice: {self.slices[i]}")
                

                




    