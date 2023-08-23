# AviatorStratChecker

[![Ruff](https://github.com/luisrx7/AviatorStratChecker/actions/workflows/ruff.yml/badge.svg)](https://github.com/luisrx7/AviatorStratChecker/actions/workflows/ruff.yml)
[![build](https://github.com/luisrx7/AviatorStratChecker/actions/workflows/tests.yml/badge.svg)](https://github.com/luisrx7/AviatorStratChecker/actions/workflows/tests.yml)

![AviatorStratChecker Cover](https://github.com/luisrx7/AviatorStratChecker/blob/main/assets/aviator-cover.webp)


Welcome to the AviatorStratChecker repository! This project aims to provide a powerful script for efficiently scraping data from the Aviator game on 22bet. By utilizing the scraped data, you can develop and test your own strategies against historical results without the need to wager any real money. We encourage your active participation by opening issues and submitting pull requests to enhance the project.

## Features

- Effortlessly scrape Aviator game data from 22bet.
- Design, simulate, and fine-tune strategies using historical data.
- Automatically bet using your own strategies.
- Collaborate with the community by contributing to the project.

## Getting Started

To set up and use AviatorStratChecker, follow these simple steps:

1. **Create a Virtual Environment:**

   ```bash
   python -m venv .venv
   ```

2. **Activate the virtual environment:**
   ```bash
   #on Windows
   .venv\Scripts\activate
   ```
   ```bash
   #on Linux
   source .venv/bin/activate
   ```


3. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a file named creds.py and add your login credentials:**
   ```python
   username = "your-email"
   password = "your-password"
   ```

5. **Install docker and docker-compose:**
   - [Docker](https://docs.docker.com/get-docker/)
   - [Docker Compose](https://docs.docker.com/compose/install/)


6. **Run Selenium using Docker:**
   ```bash
   docker-compose up
   ```


7. **Execute the script to start gathering live results:**
   ```bash
   python scrape.py
   ```




## To test Strategies

1. **Edit the file strats/custom_strats.py to add your strategies:**
   ```python
   class ExampleStrat(Strat):

    def on_win(self):
        super().on_win()

        self.bet = self.base_bet * 1.5

    def on_lose(self):
        super().on_lose()
        
        self.bet = self.base_bet
   ```

2. **Edit the checker.py script to test your new strat**

3. **Run the checker.py script to test your strat:**
   ```bash
   python checker.py
   ```


## After finding a good strategy

1. **Edit the file autobet.py to add your strategy:**
   ```python
   from strats.custom_strats import BestStrat
   
   def main():
    strat = BestStrat(
        description="BestStrat - Example",
        start_balance=3000,
        base_bet=0.1,
        max_bet=0.5,
        multiplier=1.9,
        max_bets=10000,
    )
   ```
2. **Run the autobet.py script to start betting:**
   ```bash
   python autobet.py
   ```

## TODO
   - Add tests to the existing Strats
   - Add tests to the code
   - Find some way to scrape past data from the game (maybe using requests)
   - Add a way to save the data to a database instead of a csv file
   - Add a way to compare strategies
   - Add better indicators to the strategies to help the user to decide which one to use


## Contributing
We welcome contributions! If you encounter any issues or have suggestions, please open an issue or submit a pull request.


