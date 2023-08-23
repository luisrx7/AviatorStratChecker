from strats.strats import Strat
from strats.exceptions import MaxBetsReached, InsufficientFunds

import logging
import random
from rich import print

import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)



class Strat_checker():
    def __init__(self, strat:Strat, results, slices=[]) -> None:
        self.strat = strat
        self.slices = slices
        self.strat_reports_as_string = []
        self.strat_reports = []

        self.results = results



    @staticmethod
    def slice_results_with_overlap(count, max_bets, results_length, overlap_percent):
        slices = []
        min_overlap = int(max_bets * overlap_percent)
        
        for i in range(count):
            if i == 0:
                start_index = random.randint(0, int(results_length / 2))
            else:
                previous_start, previous_end = slices[i - 1]
                potential_start = previous_end - min_overlap
                start_index = random.randint(min(previous_start, potential_start), results_length - max_bets)
                
            end_index = start_index + max_bets
            slices.append((start_index, end_index))
        
        return slices

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
    
        
        
    
    
    

    def report_as_string(self):
        print(f"\nStrategy: {self.strat.description}")
        for report in self.strat_reports_as_string:
            print(report)            

    def report(self):
        avg_won = 0
        avg_final_balance = 0
        avg_highest_balance = 0
        avg_lowest_balance = 0


        runs_with_negative_balance = 0
        runs_backrupt = 0

        for report in self.strat_reports:
            avg_won += report["won"]
            avg_final_balance += report["final_balance"]
            avg_highest_balance += report["highest_balance"]
            avg_lowest_balance += report["lowest_balance"]

            if report["final_balance"] < report["start_balance"]:
                runs_with_negative_balance += 1
            if report["final_balance"] <= report["base_bet"]:
                runs_backrupt += 1


        avg_won = avg_won / len(self.strat_reports)
        avg_final_balance = avg_final_balance / len(self.strat_reports)
        avg_highest_balance = avg_highest_balance / len(self.strat_reports)
        avg_lowest_balance = avg_lowest_balance / len(self.strat_reports)

        return {
            "strat_name": self.strat.description,
            "avg_won": avg_won,
            "avg_final_balance": avg_final_balance,
            "avg_highest_balance": avg_highest_balance,
            "avg_lowest_balance": avg_lowest_balance,
            "runs_with_negative_balance": runs_with_negative_balance,
            "runs_backrupt": runs_backrupt,

        }
    @staticmethod
    def filter_n_elements(arr,n):
        result = [x for x in arr if x % n == 0]
        return result
    
    def plot_balance_history(self,clear:bool=False,run_number:int=-1):
        color = ["blue","red","green","yellow","black","orange","purple","pink","brown","gray"]

        upper_bound = self.slices[run_number][1] if len(self.strat.balance_history) == self.slices[run_number][1] else self.slices[run_number][0] + len(self.strat.balance_history)  
        x_axis = range(self.slices[run_number][0],upper_bound )

        #on the first plot use balance_history , on the second use bet_distribution
        # Initialise the subplot function using number of rows and columns
        figure, axis = plt.subplots(1, 2)

        axis[0].plot(x_axis,self.strat.balance_history,color=color[run_number])
        axis[0].set_ylabel('balance')
        axis[0].set_xlabel('bet number')
        axis[0].set_title(f"{self.strat.description} - run {run_number+1}\nslice: {self.slices[run_number]}")


        axis[1].bar(list(self.strat.bet_distribution.keys()),
                    list(self.strat.bet_distribution.values()),
                    width=round(self.strat.base_bet/2,2),
                    ec="black" )
        axis[1].set_xlabel("Bet Amount")
        axis[1].set_ylabel("Frequency")
        axis[1].set_title(f"Distribution of Bets - run {run_number+1}")

        # # Adding text labels on top of each bar
        for bet, freq in self.strat.bet_distribution.items():
            axis[1].text(bet, freq, str(freq), ha="center", va="bottom")

        plt.show()
        
        #clear the plot
        if clear:
            plt.clf()


    def get_slices(self):
        return self.slices
    
    def set_slices(self,slices):
        self.slices = slices
    

    def run(self,count:int=1,random_slice:bool=True,plot_graph:bool=False):
        '''
        run the strat count times
        if random_slice is True, slice the results in a random places 
        count must be greater than 1 if random_slice is True
        '''
        
        self.strat.balance_history = []

        
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
                logger.info(f"max bets reached or insufficient funds  strat: {self.strat.description} - run {i+1}")
                pass
            
            except Exception as e:
                logging.error(e)
            
            finally:
                self.strat_reports_as_string.append(self.strat.report_as_string() + f"slice: {self.slices[i]}")
                self.strat_reports.append(self.strat.report())

            if plot_graph:
                self.plot_balance_history(run_number=i)

                




    