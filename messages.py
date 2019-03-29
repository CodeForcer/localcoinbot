from emoji import emojize

msg_start = emojize(
    'Hi! My name is <b>LocalCoinBot</b>. I\'m already started :smiley:',
    use_aliases=True)

msg_admins = emojize(
    'The following users are the <b>ONLY</b> admins in this group. Many scammers will attempt to impersonate admins, so always verify by clicking on one of the following profile links. Do <b>NOT</b> trust anyone else or you will be scammed:\n',
    use_aliases=True)

msg_price = emojize(
    '<b>:moneybag::moneybag: LocalCoinSwap Token Price :moneybag::moneybag:</b>\n\n:fire: The current price of LCS in USD value is: {} :fire:\n\n:fire: In the last 24 hours the price has changed: {} :fire:',
    use_aliases=True)

msg_price_error = emojize(
    'I was unable to grab the latest price data. Might be a good idea to <a href="https://support.localcoinswap.com/">Contact Support</a>',
    use_aliases=True)

msg_welcome = emojize(
    '<b>Welcome {{username}}!</b>\nYou can start trading 21+ cryptocurrencies, with 250+ payment methods, at <a href="https://localcoinswap.com/">LocalCoinSwap.Com</a>. Signup is instant with no KYC.\nFor any other questions, or just to chat with the community, this group is the place to be.\nPS: Read the pinned post to avoid scammers!',
    use_aliases=True)
    
msg_communities = emojize(
    '<b>:clap::clap: LocalCoinSwap.Com Official Communities :clap::clap:</b>\n\n:zap: <a href="https://localcoinswap.com/">LocalCoinSwap Exchange</a>\n:zap: <a href="https://t.me/localcoinswap">LocalCoinSwap English Telegram</a>\n:zap: <a href="https://t.me/localcoinswap_rus">LocalCoinSwap Russian Telegram</a>\n:zap: <a href="https://t.me/localcoinswap_esp">LocalCoinSwap Spanish Telegram</a>\n:zap: <a href="https://t.me/localcoinswap_ar">LocalCoinSwap Arabic Telegram</a>\n:zap: <a href="https://twitter.com/Localcoinswap_">LocalCoinSwap Official Twitter</a>\n:zap: <a href="https://www.facebook.com/localcoinswap/">LocalCoinSwap Facebook Page</a>\n:zap: <a href="https://www.reddit.com/user/Localcoinswap/">LocalCoinSwap Subreddit</a>',
    use_aliases=True)
    
msg_not_private = emojize(
    'I\'m feeling a little shy, and this isn\'t a good place to chat :sweat: Message me privately so we can get better acquainted',
    use_aliases=True)

msg_not_supergroup = emojize(
    'I\'d prefer to do this kind of thing in public, just to make sure you aren\'t pushing my circuits too hard :sweat:',
    use_aliases=True)
    
msg_punished = emojize(
    '{} has been a very naughty meat-sack. I\'m going to put them in timeout for 24 hours',
    use_aliases=True)
    
msg_forgiven = emojize(
    '{} your sins have been forgiven. Thanks to the mercy of the LocalCoinSwap team your posting rights are unrestricted',
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