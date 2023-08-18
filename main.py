from aviator import Aviator

import rich
import rich.traceback
rich.traceback.install()


def main():
    try:
        aviator = Aviator(debug=True)
        aviator.login()
        aviator.go_to_game()


        while aviator.in_game():
            aviator.wait_for_game_to_finish()
            aviator.add_to_log(aviator.get_last_game_result())
    except Exception as e:
        rich.print_exception(show_locals=True)

    finally:
        aviator.close()

if __name__ == "__main__":
    main()