import logging

import rich
import rich.console
import rich.traceback

from aviator import Aviator

rich.traceback.install()

console = rich.console.Console()


logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG, datefmt='%m/%d/%Y %I:%M:%S')


def signal_handler(sig, frame):
    global stop
    print('You pressed Ctrl+C!')
    stop = True
    # sys.exit(0)


stop = False

def main():
    
    while stop is False:
        try:
            aviator = Aviator(debug=True,demo=False,remote_address="192.168.2.150")
            aviator.login()
            aviator.go_to_game()


            while aviator.in_game() and stop is False:
                if aviator.disconnected():
                    break
                aviator.wait_for_game_to_finish()
                aviator.add_to_log(aviator.get_last_game_result())
        except Exception as e:
            console.print_exception(show_locals=True)
            logging.error(e)
        finally:
            aviator.close()

if __name__ == "__main__":
    main()