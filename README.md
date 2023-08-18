# AviatorStratChecker

Welcome to the AviatorStratChecker repository! This project aims to provide a powerful script for efficiently scraping data from the Aviator game on 22bet. By utilizing the scraped data, you can develop and test your own strategies against historical results without the need to wager any real money. We encourage your active participation by opening issues and submitting pull requests to enhance the project.

## Features

- Effortlessly scrape Aviator game data from 22bet.
- Design, simulate, and fine-tune strategies using historical data.
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

5. **Run Selenium using Docker:**
   ```bash
   docker-compose up
   ```


5. **Execute the script:**
   ```bash
   python main.py
   ```


## Contributing
We welcome contributions! If you encounter any issues or have suggestions, please open an issue or submit a pull request.


