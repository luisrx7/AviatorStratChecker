profile_path = "/tmp/.com.google.Chrome.4QE50k"


#game

play_button_of_first_search_result = '//*[@id="games"]/div/div[1]/button'
play_free_button_of_first_search_result = '//*[@id="games"]/div/div[1]/div[2]/div[1]/button'

game_name = '//*[@id="slots"]/div[2]/div[1]/div[1]'

last_game_results = 'body > app-root > app-game > div > div.main-container > div.w-100.h-100 > div > div.game-play > div.result-history.disabled-on-game-focused.my-2 > app-stats-widget > div > div.payouts-wrapper > div > app-bubble-multiplier:nth-child($ROUND$)'
last_game_result = "/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[1]/app-stats-widget/div/div[1]/div/app-bubble-multiplier[1]/div"

open_new_window_button = '//*[@id="wrapper_game_area"]/div/ul/li[3]/a'

balance = '/html/body/app-root/app-game/div/div[1]/div[1]/app-header/div/div[2]/div[1]/div[1]/div/span[1]'


#bets


bet_type_button = '/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[3]/app-bet-controls/div/app-bet-control[1]/div/app-navigation-switcher/div/button[2]'
auto_cashout_button = '/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[3]/app-bet-controls/div/app-bet-control[1]/div/div[3]/div[2]/div[1]/app-ui-switcher'
place_bet_button = '/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[3]/app-bet-controls/div/app-bet-control[1]/div/div[1]/div[2]/button'

bet_amount_input_box = '/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[3]/app-bet-controls/div/app-bet-control[1]/div/div[1]/div[1]/app-spinner/div/div[2]/input'
multiplier_input_box = '/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[3]/app-bet-controls/div/app-bet-control[1]/div/div[3]/div[2]/div[2]/div/app-spinner/div/div[2]/input'