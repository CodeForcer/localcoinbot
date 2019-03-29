from emoji import emojize

msg_start = emojize(
    'Hi! My name is LocalCoinBot. I\'m already started :smiley:',
    use_aliases=True)

msg_admins = emojize(
    'The following users are the ONLY admins in this group. Do not trust anyone else:\n',
    use_aliases=True)

msg_price = emojize(
    'The current price of LCS in USD value is: {}\n\nIn the last 24 hours the price has changed: {}',
    use_aliases=True)

msg_price_error = emojize(
    'I was unable to grab the latest price data',
    use_aliases=True)

msg_welcome = emojize(
    '<b>Welcome {{username}}!</b>\nYou can start trading 21+ cryptocurrencies, with 250+ payment methods, at <a href="https://localcoinswap.com/">LocalCoinSwap.Com</a>. Signup is instant with no KYC.\nFor any other questions, or just to chat with the community, this group is the place to be.\nPS: Read the pinned post to avoid scammers!',
    use_aliases=True)
    
msg_communities = emojize(
    '<b>--- LocalCoinSwap.Com Official Communities ---</b>\n<a href="https://localcoinswap.com/">LocalCoinSwap Exchange</a>\n<a href="https://t.me/localcoinswap">LocalCoinSwap English Telegram</a>',
    use_aliases=True)
    
msg_not_private = emojize(
    'I\'m feeling a little shy, and this isn\'t a good place to chat :sweat: Message me privately so we can get better acquainted',
    use_aliases=True)
    
msg_punished = emojize(
    '{} has been a very naughty meat-sack. I\'m going to put them in timeout for 24 hours',
    use_aliases=True)
    
msg_forgiven = emojize(
    '{} your sins have been forgiven. Thanks to the mercy of the LocalCoinSwap team your posting rights are unrestricted',
    use_aliases=True)
    
msg_promo_into = emojize(
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