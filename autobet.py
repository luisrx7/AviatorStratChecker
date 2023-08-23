import logging
import time

import rich
import rich.console
import rich.traceback
import sys

from aviator import Aviator
from strats.custom_strats import DAlembertStrat

rich.traceback.install()
console = rich.console.Console()


logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.INFO, datefmt='%m/%d/%Y %I:%M:%S', filename="autobet.log")

logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))


def signal_handler(sig, frame):
    global stop
    print('You pressed Ctrl+C!')
    stop = True
    # sys.exit(0)


stop = False




def main():
    strat = DAlembertStrat(
        description="DAlembertStrat",
        start_balance=3000,
        base_bet=0.1,
        max_bet=0.5,
        multiplier=1.9,
        max_bets=10000,
    )
    
    while stop is False:
        try:
            aviator = Aviator(debug=True, strat=strat)
            aviator.login()
            aviator.go_to_game()
            time.sleep(3)
            aviator.setup_auto_bet()


            while aviator.in_game() and stop is False:
                aviator.wait_for_game_to_finish()
                last_result = aviator.get_last_game_result()
                aviator.process_bet(float(last_result))
                aviator.add_to_log(last_result)
                logging.info(f"balance: {aviator.get_balance()}")
        except Exception as e:
            console.print_exception(show_locals=True)
            logging.error(e)
        finally:
            aviator.close()

if __name__ == "__main__":
    main()