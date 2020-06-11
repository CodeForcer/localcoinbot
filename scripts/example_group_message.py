import telegram
from emoji import emojize

TOKEN = ''
GROUP_ID = ''
HTML_MESSAGE = (
    '<b>LocalCoinSwap Announces Next Non-Custodial Implementation</b>\n\n'
    'https://blog.localcoinswap.com/localcoinswap-builds-on-kusama/'
)

bot = telegram.Bot(token=TOKEN)

message = emojize(HTML_MESSAGE, use_aliases=True)

bot.sendMessage(
    chat_id=GROUP_ID,
    text=HTML_MESSAGE,
    parse_mode='HTML')
