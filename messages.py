from emoji import emojize

msg_start = emojize(
    'Hi! My name is <b>LocalCoinBot</b>. I\'m the newest member of the LocalCoinSwap team!\n\nI\'m here to help moderate the chat group and handle promotional competitions. I\'m not always perfect just because I\'m a robot, so if I do something weird then don\'t be afraid to let my bosses know :smiley:\n\nThere\'s a bunch of cool things I can already do:\n/start   Show this message\n/admins   Show the admins of this group\n/communities   List the official LocalCoinSwap communities\n',
    use_aliases=True)

msg_admins = emojize(
    'The following users are the <b>ONLY</b> admins in this group. Many scammers will attempt to impersonate admins, so always verify by clicking on one of the following profile links. Do <b>NOT</b> trust anyone else or you will be scammed:\n',
    use_aliases=True)

msg_welcome = emojize(
    '<b>Welcome {{username}} :clap::clap:</b>\n\n:star2: Trade a Range of Cryptocurrencies\n:star2: Use 250+ Payment Methods\n:star2: Instant Signup with No Delays\n:star2: Trade Your Way at <a href="https://localcoinswap.com/">LocalCoinSwap</a>\n\n💫 If you have questions, need some help, or just want to chat with the community, this group is the place to be. Read the pinned post to avoid scammers!\n\n<b>⚠️ Please select the green circle 🟢 to prove you are human!</b>',
    use_aliases=True)

msg_communities = emojize(
    '<b>:clap::clap: LocalCoinSwap.Com Official Communities :clap::clap:</b>\n\n:zap: <a href="https://localcoinswap.com/">LocalCoinSwap Exchange</a>\n:zap: <a href="https://t.me/localcoinswap">LocalCoinSwap English Telegram</a>\n:zap: <a href="https://t.me/localcoinswap_rus">LocalCoinSwap Russian Telegram</a>\n:zap: <a href="https://t.me/localcoinswap_esp">LocalCoinSwap Spanish Telegram</a>\n:zap: <a href="https://t.me/localcoinswap_ar">LocalCoinSwap Arabic Telegram</a>\n:zap: <a href="https://twitter.com/Localcoinswap_">LocalCoinSwap Official Twitter</a>\n:zap: <a href="https://www.facebook.com/localcoinswap/">LocalCoinSwap Facebook Page</a>\n:zap: <a href="https://www.reddit.com/user/Localcoinswap/">LocalCoinSwap Subreddit</a>',
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
