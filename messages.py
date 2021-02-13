from emoji import emojize

msg_start = emojize(
    'Hi! My name is <b>LocalCoinBot</b>\n\nI\'m here to help moderate the chat group and handle promotional competitions. I\'m not always perfect just because I\'m a robot, so if I do something weird then don\'t be afraid to let my bosses know :smiley:\n\nThere\'s a bunch of cool things I can already do:\n/start - Show this message\n/admins - Show the group admins\n/communities - Official communities\n/support - Find Help or support\n/socials - Find us on social media\n/contract - LCS token smart contract\n/gas - Ethereum Gas Estimates\n/exchanges - Places to trade LCS\n/price - Show crypto market stats e.g. bitcoin usd',
    use_aliases=True)

msg_admins = emojize(
    'The following users are the <b>ONLY</b> admins in this group. Many scammers will attempt to impersonate admins, so always verify by clicking on one of the following profile links. Do <b>NOT</b> trust anyone else or you will be scammed:\n\n',
    use_aliases=True)

msg_welcome = emojize(
    '<b>Welcome {} :clap::clap:</b>\n\n:star2: Trade a Range of Cryptocurrencies\n:star2: Use 250+ Payment Methods\n:star2: Instant Signup with No Delays\n:star2: Trade Your Way at <a href="https://localcoinswap.com/">LocalCoinSwap</a>\n\n💫 If you have questions, need some help, or just want to chat with the community, this group is the place to be. Read the pinned post to avoid scammers!\n\n<b>⚠️ Please select the {} to prove you are human!</b>',
    use_aliases=True)

msg_communities = emojize(
    '<b>LocalCoinSwap Official Communities</b>:clap::clap:\n:zap:<a href="https://t.me/localcoinswap">LocalCoinSwap English Telegram</a>\n:zap: <a href="https://t.me/localcoinswap_esp">LocalCoinSwap Spanish Telegram</a>',
    use_aliases=True)

msg_not_private = emojize(
    'Congratulations on your completed trade. To register for the promotion and receive your BTC, <a href="https://t.me/LocalCoinSwapsBot">message me privately</a> and enter /start to begin',
    use_aliases=True)

msg_not_supergroup = emojize(
    'I\'d prefer to do this kind of thing in public, just to make sure you aren\'t pushing my circuits too hard :sweat:',
    use_aliases=True)

msg_punished = emojize(
    '{} has been a very naughty meat-sack. I\'m going to put them in timeout for 24 hours :thumbsdown:',
    use_aliases=True)

msg_forgiven = emojize(
    '{} your sins have been forgiven. Thanks to the mercy of the LocalCoinSwap team your posting rights are unrestricted :facepunch:',
    use_aliases=True)

msg_only_admins = emojize(
    'Sorry meat-sack, only admins can do this',
    use_aliases=True)

msg_subscribe = emojize(
    'Hey {}. You have just subscribed to receive Telegram notifications. Your unique chat ID is {}. Don\'t foget to check that I\'m not muted!',
    use_aliases=True)

msg_default_start = emojize(
    'Hi {}! I can use this private conversation to send you notifcations about new trades and messages, so you don\'t miss out. To activate this feature, visit your preferences page on the LocalCoinSwap exchange',
    use_aliases=True)

msg_subscribe_error = emojize(
    'There was some kind of error registering you with the exchange to receive notifications. Did you follow the correct link? Please raise a support ticket if this issue persists',
    use_aliases=True)

msg_contract = emojize(
    '📃 <a href="https://etherscan.io/address/0xaa19961b6b858d9f18a115f25aa1d98abc1fdba8">LCS Token Smart Contract</a>',
    use_aliases=True)

msg_exchanges = emojize(
    '<b>Places to Trade LCS Tokens</b> 👀\n🔹<a href="https://localcoinswap.com/buy-sell/LCS/">LocalCoinSwap</a>\n🔹<a href="https://www.hotbit.io/exchange?symbol=LCS_BTC">Hotbit</a>\n🔹<a href="https://app.uniswap.org/#/swap?inputCurrency=0xaa19961b6b858d9f18a115f25aa1d98abc1fdba8">Uniswap</a>\n🔹<a href="https://forkdelta.app/#!/trade/0xaa19961b6b858d9f18a115f25aa1d98abc1fdba8-ETH">ForkDelta</a>',
    use_aliases=True)

msg_help = emojize(
    '<b>Need Help? 🤷‍♂️</b>\nContact us via our <a href="https://support.localcoinswap.com/hc/en-us">Support Portal</a>',
    use_aliases=True)

msg_socials = emojize(
    '<b>LocalCoinSwap on Social Media 💬</b>\n🔸<a href="https://localcoinswap.com/">Facebook</a>\n🔸<a href="https://twitter.com/Localcoinswap_">Twitter 🇬🇧</a>\n🔸<a href="https://twitter.com/LocalCoinSwapES">Twitter 🇪🇸</a>\n🔸<a href="https://www.linkedin.com/company/localcoinswap/">LinkedIn</a>\n🔸<a href="https://www.reddit.com/r/LocalCoinSwap/">Reddit</a>',
    use_aliases=True)

msg_gas = emojize(
    "<b>Estimated Ethereum Gas Prices</b>\n\n🟢 Fast: <code>{}</code> Gwei\n🟡 Standard: <code>{}</code> Gwei\n🔴 Low: <code>{}</code> Gwei\n\nFor the most accurate estimates:\nhttps://ethgasstation.info/",
    use_aliases=True)

msg_stats_fail = emojize(
    "<b>Unable to Fetch Price</b> 🤔\n\nPlease check your request and only use full coin name with fiat ticker all in lowercase, e.g. bitcoin usd. You wont be able to price check everything, but it will work for most things.\n\n",
    use_aliases=True)

msg_crypto_stats = emojize(
    "📊 <b>{}/{}</b>\nPrice:\n<code>{} {}</code>\nVolume:\n<code>{}</code>\nMarket Cap:\n<code>{}</code>\nChange:\n<code>{}</code>\n",
    use_aliases=True)

msg_stats_price = emojize(
    "📊 <b>{}/{}</b>\n<code>{}</code> {}",
    use_aliases=True)

msg_translate = emojize(
    "<b>🌎 Attempting Translation:</b>\n{}",
    use_aliases=True)

msg_translate_failed = emojize(
    "<b>🌎 Translation Failed:\n</b>Please check your request and try again later.\n",
    use_aliases=True)