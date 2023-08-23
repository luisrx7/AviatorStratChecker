from browser.browser import Browser
import helium 
import aviator.vars as vars
import creds as creds
from selenium.webdriver.common.by import By
import time
from datetime import datetime 

from strats.strats import Strat

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException

import logging

logger = logging.getLogger(__name__)

class Aviator(Browser):
    '''
    this class will interact with the browser

    '''

    def __init__(self, headless=False, test=False, remote_driver=True,
                remote_address="127.0.0.1",remote_port=4446, use_cookies=False,
                debug=False,strat: Strat = None):
        super().__init__(headless= headless, test=test, remote_driver=remote_driver,
                remote_address=remote_address,remote_port=remote_port,
                  use_cookies=use_cookies, profile_path=vars.profile_path)
        
        self.debug = debug
        self.strat = strat
        
        if self.strat is not None:
            self.strat.reset()

        helium.set_driver(self.driver)
        


    def login(self):
        helium.go_to("https://22bet-b.com")
        if not self.logged_in():
            helium.click("LOG IN")
            helium.write(creds.username, into="ID or Email")
            helium.write(creds.password, into="Password")
            helium.click("Remember")
            helium.click("LOG IN")
            input("press enter to continue")
        
        

    def logged_in(self):
        if self.debug:
            logger.debug("checking if logged in")
        element = helium.S("#user-money")
        if element.exists():
            if self.debug:
                logger.debug("logged in")
            return True
        else:
            if self.debug:
                logger.debug("not logged in")
            return False
        

    def in_game(self):
        '''
        check if we are in game
        '''
        if self.debug:
            logger.debug("checking if in game")

        element = self.find_elements(By.XPATH, vars.game_name, timeout=0.5)
        if element or self.driver.title == "Aviator":
            if self.debug:
                logger.debug("in game")
            return True

        if self.debug:
            logger.debug("not in game")
        return False            
    
    def get_last_game_result(self):
        '''
        get last game result
        '''
        # if self.debug:
        #     logger.debug("getting last game result")

        element = self.find_elements(By.XPATH, vars.last_game_result, timeout=1)
        
        if element is not None:
            return element.text.strip().replace("x", "")


        results = self.get_game_results()
        if len(results) > 0:
            return results[0]

    def process_bet(self, result):
        '''
        check if a strat is defined
        if it is, use it to calculate the next bet
        if not warn the user that a strat is not defined
        '''
        if self.debug:
            logger.debug(f"processing bet for result {result}")
        if self.strat is None:
            logger.debug("WARNING: no strat defined")
            return False

        self.strat.calculate_bet(result)
        if self.debug:
            logger.debug(f"bet: {self.strat.bet}, multiplier: {self.strat.multiplier}")

        if self.strat.bet == 0 or self.strat.multiplier == 0:
            if self.debug:
                logger.debug("bet or multiplier is 0, not placing bet")
            return False        

        if self.place_bet(self.strat.bet, self.strat.multiplier) is False:
            if self.debug:
                logger.debug("could not place bet")
            return False
        
        self.strat.gamble()


    def get_game_results(self):
        '''
        get game result
        '''


        # Find the div element with class "payouts-block"
        payouts_div = self.find_elements(By.CLASS_NAME, "payouts-block")
        if payouts_div is None:
            if self.debug:
                logger.debug("could not get game results")
            return []

        # Find all elements with class "bubble-multiplier" within the payouts div
        multiplier_elements = payouts_div.find_elements(By.CLASS_NAME, "bubble-multiplier")

        results = []
        # Extract the values
        try:
            for element in multiplier_elements:
                results.append(element.text.strip().replace("x", ""))
        except StaleElementReferenceException or NoSuchElementException:
            #refresh the page
            self.driver.refresh()
            pass
        



            
        if len(results) > 0:
            # if self.debug:
            #     logger.debug("got game results")
            return results
        else:
            if self.debug:
                logger.debug("could not get game results")


        return []


    def get_balance(self):
        '''
        get balance
        '''
        if self.debug:
            logger.debug("getting balance")
        element = self.find_elements(By.XPATH, vars.balance)
        #element is a span with the balance
        if element:
            if self.debug:
                logger.debug("got balance")
            return element.text
        else:
            if self.debug:
                logger.debug("could not get balance")
            return None


    def disconnected(self):
        '''
            check if disconnected warning is displayed
        '''
        disconnected_element = self.find_elements(By.XPATH, vars.disconnected_warning, timeout=0.5)
        if disconnected_element is not None:
            return True
        return False

    def wait_for_game_to_finish(self):
        '''
        wait for game to finish
        since the game is in a loop, we need to wait for the game to finish
        the only way to check if the game is finished is to check if we have
        a new result different from the last one
        '''

        if self.debug:
            logger.debug("waiting for game to finish")
        last_result = self.get_last_game_result()
        while True:
            if self.disconnected():
                if self.debug:
                    logger.debug("disconnected")
                break
            result = self.get_last_game_result()
            if result is not None:
                if result != last_result :
                    break
            if self.debug:
                logger.debug(".", end="")
            time.sleep(0.1)
        if self.debug:
            logger.debug("\ngame finished")
    
    def add_to_log(self, result):
        '''
        add result to results.txt in this 
        format timestamp (format dd-mm-yyyy hh:mm:ss),result
        '''
        if self.debug:
            logger.debug(f"adding result {result}  to log")
        with open("results.txt", "a") as f:
            f.write(f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')},{result}\n")


    def setup_auto_bet(self):
        '''
        click the buttons to setup auto cashout
        '''
        if self.debug:
            logger.debug("setting up auto bet")

        if self.click_button(vars.bet_type_button) is False:
            if self.debug:
                logger.debug("could not click bet type button")
            return False
        if self.click_button(vars.auto_cashout_button) is False:
            if self.debug:
                logger.debug("could not click auto cashout button")
            return False
        

    def place_bet(self,amount, multiplier):
        '''
        place bet with amount and multiplier
        '''
        if self.debug:
            logger.debug(f"setting bet amount to {amount} at multiplier {multiplier}")


        if self.send_keys(vars.bet_amount_input_box, str(amount)) is False:
            if self.debug:
                logger.debug("could not set bet amount")
            return False

        if self.send_keys(vars.multiplier_input_box, str(multiplier)) is False:
            if self.debug:
                logger.debug("could not set multiplier")
            return False
        
        if self.click_button(vars.place_bet_button) is False:
            if self.debug:
                logger.debug("could not click place bet button")
            return False
        
        return True


    def go_to_game(self):
        wait = WebDriverWait(self.driver, 10)

        helium.go_to("https://22bet-b.com/slots")
        helium.write("AVIATOR", into="SEARCH")
        #sleep for 2 seconds to let the search results load
        time.sleep(2)
        self.click_button(vars.play_free_button_of_first_search_result)

        #wait for the game to load
        time.sleep(2)

        # Store the ID of the original window
        original_window = self.driver.current_window_handle

        # Check we don't have other windows open already
        assert len(self.driver.window_handles) == 1

        # Click the link which opens in a new window
        self.click_button(vars.open_new_window_button)

        # Wait for the new window or tab
        wait.until(EC.number_of_windows_to_be(2))

        # Loop through until we find a new window handle
        for window_handle in self.driver.window_handles:
            if window_handle != original_window:
                self.driver.switch_to.window(window_handle)
                break

        # Wait for the new tab to finish loading content
        wait.until(EC.title_is("Aviator"))

        #maximize window
        self.driver.maximize_window()
    
        #wait for the game to open in a new window
        time.sleep(2)



