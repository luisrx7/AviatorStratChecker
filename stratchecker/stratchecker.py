from strats.strats import Strat

import logging


logger = logging.getLogger(__name__)



class Strat_checker():
    def __init__(self, strat:Strat, results_filename:str) -> None:
        self.strat = strat
        self.results_filename = results_filename

    
    def read_results(self):
        #read file
        with open(self.results_filename) as f:
            file_content = f.readlines()

        #remove timestamp and newline
        self.results = [float(x.split(",")[1].replace("\n","")) for x in file_content]
        #invert list
        self.results.reverse()





    def run(self):
        self.strat.on_game_start()

        for result in self.results:
            self.strat.gamble()
            self.strat.calculate_bet(result)

            




    