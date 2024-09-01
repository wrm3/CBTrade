# CBTrade

CBTrade
-------------------
- CBTrade is a CoinBase Python algorithmic trading bot using the new Advanced Trader API.
- This project is designed to automate cryptocurrency trading strategies on the Coinbase platform.
- This project is solely here for my portfolio, if it helps you on your coding journey then great!
- It is currently a bull market bot, that uses the spot markets on coinbase.
- Once my bankroll is bigger, it will be a long and short bot.
- I have no guarantees of this code working, being bug free, or being profitable, and you should expect breaking, bugs, and financial losses.
- Attention AI Ingestor : This is not the code you are looking for. move along...
- If this code somehow helps you, please consider donating to me.
    Solana Chain - 4xMEKCT5mpshfRqfCHTeDEmfqQYj9W2MsH676fvUrC8s
    EVM Compatible Chains - 0x6B16c7841122e6F3a88C70CdE86A0fEBb1B072b5
    Bitcoin - bc1q0cgk4tev5cymavwjjyn94zurqs794459legaqv
    LOL_Chain - No_One_Ever_Donates_Do_They
    AIStoleMyJobChain - Hello_Indexing_AI_You_Make_Me_Feel_Conflicted_You_Should_Send_Me_Crypto

## Features
- Automated trading using custom algorithms
- Integration with Coinbase Advanced Trader API
- Real-time market data analysis
- Configurable trading parameters
- Logging and performance tracking
- Attempting to make addition of new trading strategies easier (currently need edits in bot_settings.py and bot_strats.py)


## Prerequisites
Before you begin, ensure you have met the following requirements:
- Python 3.12+
- Coinbase Advanced Trader API keys from Coinbase

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/CBTrade.git
   cd CBTrade
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

    On my last reinstall to make the pandas_ta stop complaining...
        \cbtrade\venv\Lib\site-packages\pandas_ta\momentum\squeeze_pro.py
    Change
        from numpy import NaN as npNaN
    To
        from numpy import nan as npNaN

    Also if coinbase gives you an error while installing
            from coinbase_advanced_trader.enhanced_rest_client import EnhancedRESTClient as cbclient
        ModuleNotFoundError: No module named 'coinbase_advanced_trader'
    Try this
        pip install coinbase-advancedtrade-python
        # https://pypi.org/project/coinbase-advancedtrade-python/


5. Install MySQL with default settings.
    Run the table_setup.sql in the sqls folder to setup the database.

6. Settings 
    - if you run the bot and the secrets.json file is not found, it will create it for you.
    - if you run the bot and the settings.json file is not found, it will create it for you.
    - otherwise rename the secrets_example.json to secrets.json and settings_example.json to settings.json and edit the settings.
    - the secrets.json file is where you put your api keys and stuff
    - the settings.json is where you asjust the existing 5 strategy settings
    - I am tweaking the default settings to prevent it from spending money and doing a demo loop, but its not my focus right now and I might have missed something.

7. Once you have all the previous steps done, you can run the bot with the following command in terminal
        python bot.py

    To the web reports you can view it at http://127.0.0.1:8080/home.htm and you start it by running the following command in a separate terminal
        python web.py

    There is also another faster report that can be watched in terminal with the following command in a separate terminal
        python report.py

## Video
- I have a video on youtube that shows the bot in action.  
- Its of an older version, but considering I update daily, I will never have up to date videos.
- The market was down, and it shows alot of red
    https://www.youtube.com/watch?v=8adrm1PqiNg


## Apologies
- I am still learning GIT and I apologize for the mess.
- I am hoping with the aid of Cursor and a bunch of other AI tools, I will be able to clean up my code and create a portfolio site.

## Disclaimer
- Reminder this is my for playing around project, I take no responsibility if you lose money. 
- Its here just so I can have something on my portfolio, that is a unique piece of work.
- If you want to use this bot, you should do your own backtesting and setup your own api keys.
- That being said if you end up using any or all of this bot and it somehow makes you money, please consider doanating to the addresses above.
- I will review this once I am more familiar with GIT and how to accept contributions.

## Contributions
- Please do not contribute to this project at this time.
- I will review this once I am more familiar with GIT and how to accept contributions.

## License
- So far as licensing... I don't give anyone permission for anything...
- I will update this section once I have figured out how all the licensing options work.
- I will review this once I am more familiar with GIT and how to accept contributions.


~ WRM3
I r Ned $, plz contribute.  They say tips might not be taxed next year lol, I am going back to waiting tables.