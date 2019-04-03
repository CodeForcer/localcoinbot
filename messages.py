from emoji import emojize

msg_start = emojize(
    'Hi! My name is <b>LocalCoinBot</b>. I\'m the newest member of the LocalCoinSwap team!\n\nI\'m here to help moderate the chat group and handle promotional competitions. I\'m not always perfect just because I\'m a robot, so if I do something weird then don\'t be afraid to let my bosses know :smiley:\n\nThere\'s a bunch of cool things I can already do:\n/start   Show this message\n/admins   Show the admins of this group\n/price   Get the latest token price information for LCS\n/communities   List the official LocalCoinSwap communities\n',
    use_aliases=True)

msg_start_priv = emojize(
    'Hi! My name is <b>LocalCoinBot</b>. I\'m here to help you with with LocalCoinSwap promotional competitions, and provide useful information such as token prices or lists of administrators.\n\nI\'m not always perfect just because I\'m a robot, so if I do something weird then don\'t be afraid to let my bosses know :smiley:\n\nSome commands you can try are:\n/start   Show this message\n/promo5   Enter our latest promotional competition\n/admins   Show the admins of a group\n/price   Get the latest token price information for LCS (only available in public chats)\n/communities   List the official LocalCoinSwap communities\n',
    use_aliases=True)

msg_admins = emojize(
    'The following users are the <b>ONLY</b> admins in this group. Many scammers will attempt to impersonate admins, so always verify by clicking on one of the following profile links. Do <b>NOT</b> trust anyone else or you will be scammed:\n',
    use_aliases=True)

msg_price = emojize(
    '<b>:fire::fire: LocalCoinSwap Token Price :fire::fire:</b>\n\n:dollar: The current price of LCS in USD value is: {}\n\n:dollar: In the last 24 hours the price has changed: {}',
    use_aliases=True)

msg_price_error = emojize(
    'I was unable to grab the latest price data. Might be a good idea to <a href="https://support.localcoinswap.com/">Contact Support</a>',
    use_aliases=True)

msg_welcome = emojize(
    '<b>Welcome {{username}} :clap::clap:</b>\n\n:star2:Start trading 21+ cryptocurrencies, with 250+ payment methods, at <a href="https://localcoinswap.com/">LocalCoinSwap</a>\n:star2:Signup is instant with no KYC\n:star2:For any other questions, or just to chat with the community, this group is the place to be\n\nPS: Read the pinned post to avoid scammers!',
    use_aliases=True)
    
msg_communities = emojize(
    '<b>:clap::clap: LocalCoinSwap.Com Official Communities :clap::clap:</b>\n\n:zap: <a href="https://localcoinswap.com/">LocalCoinSwap Exchange</a>\n:zap: <a href="https://t.me/localcoinswap">LocalCoinSwap English Telegram</a>\n:zap: <a href="https://t.me/localcoinswap_rus">LocalCoinSwap Russian Telegram</a>\n:zap: <a href="https://t.me/localcoinswap_esp">LocalCoinSwap Spanish Telegram</a>\n:zap: <a href="https://t.me/localcoinswap_ar">LocalCoinSwap Arabic Telegram</a>\n:zap: <a href="https://twitter.com/Localcoinswap_">LocalCoinSwap Official Twitter</a>\n:zap: <a href="https://www.facebook.com/localcoinswap/">LocalCoinSwap Facebook Page</a>\n:zap: <a href="https://www.reddit.com/user/Localcoinswap/">LocalCoinSwap Subreddit</a>',
    use_aliases=True)
    
msg_not_private = emojize(
    'Congratulations on your completed trade. To register for the promotion and receive your BTC, <a href="https://t.me/LocalCoinSwapsBot">message me privately</a>',
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
    
msg_promo_intro = emojize(
    'Thank you for taking part in our promotion, please answer a couple of short questions to register your details',
    use_aliases=True)
    
msg_promo_email_prompt = emojize(
    'What is your email address which you used on the LocalCoinSwap exchange?',
    use_aliases=True)
    
msg_promo_email_given = emojize(
    'Your email address is {}? Great, lets continue!',
    use_aliases=True)
    
msg_promo_twitter_prompt = emojize(
    'What is your Twitter address you are Tweeting about LocalCoinSwap from?',
    use_aliases=True)
    
msg_promo_twitter_given = emojize(
    'Your Twitter address is {}? Great, lets continue!',
    use_aliases=True)
    
msg_promo_trade_prompt = emojize(
    'What is your url for the completed trade you wish to claim a prize for?',
    use_aliases=True)
    
msg_promo_trade_given = emojize(
    'Your trade url is {}? Great!',
    use_aliases=True)
    
msg_promo_complete = emojize(
    'The following details have been entered into our promotion:\n{}\nIt normally takes 5-7 days for prizes to be allocated. Thanks for your participation!',
    use_aliases=True)
    
msg_only_admins = emojize(
    'Sorry meat-sack, only admins can do this',
    use_aliases=True)