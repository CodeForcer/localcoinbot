Simple LocalCoinSwap group Telgram bot

Setup:
1. Create virtual env and open it:  
  ```virtualenv -p python3 venv```  
  ```source venv/bin/activate```
2. Install requirements:  
  ```pip3 install -r requirements.txt```
3. Create `settings.py` file in base directory
4. Create variables in `settings.py`:  
  TOKEN = 'token', where 'token' is the bot authentication token  
  API_KEY = 'key', where 'key' is the CoinMarketCap authentication token
5. Create CSV file for promo data:  
  ```touch PROMO5.CSV```

Testing locally:
1. Open virtualenv and then start the bot:  
  ```source venv/bin/activate```  
  ```python3 localcoinbot.py```

Remote deployment:
The included systemd service file has been tested for remote deployment.

## Example URL:

https://telegram.me/LocalCoinSwapTestBot?start=uEDbtJFHxKc