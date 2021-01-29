Simple LocalCoinSwap group Telgram bot which moderates:
https://t.me/localcoinswap (group ID -1001332456112)

Setup:
1. Create virtual env and open it:
  ```virtualenv -p python3 venv```
  ```source venv/bin/activate```
2. Install requirements:
  ```pip3 install -r requirements.txt```
3. Create `settings.py` file in base directory
4. Create variables in `settings.py`:
  TOKEN = 'token', where 'token' is the bot authentication token
  GROUP_ID = 'group id for where the bot is to be used'

Testing locally:
1. Open virtualenv and then start the bot:
  ```source venv/bin/activate```
  ```python3 localcoinbot.py```

Remote deployment:
The included systemd service file has been tested for remote deployment.

## Example URL:

https://telegram.me/LocalCoinSwapsBot?start=uEDbtJFHxKc