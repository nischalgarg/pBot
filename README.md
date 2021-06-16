# pBot

Use '/start' command (without the quotes) to start-up the bot and load the menu button.
This message can be deleted later.

The bot reads user messages in one-on-one chat by default.

If the bot is being used in a group, it can read user messages only if it has access to user messages.
This permission shall be provided by the owner of the group or by provoding admin status to the bot.
The buttons, however, shall function in the groups even without access to reading user messages.

__________________________________________________________________________________________________________________________________________________

# Button Menu Layout

The button menu has 10 buttons. The layout can be found in the [main code file](bot.py)

1) About --> Replies with the prepared text
2) Announcement --> Replies with the prepared text
3) pStake --> Provides user with the pstake information and link
4) Website --> Provides user with the official website link
5) Twitter --> Provides user with the Twitter page link
6) Discord --> Provides the user with the discord channel link
7) Blogs --> Replies with text and link to blog on Medium
8) Wallet --> Provides link to the wallet service
9) Alerts --> Notifies of autenticate channel and to beware of fake/spam channels
10) Trolls --> Picks a random meme from the "Persistence Meme Club" Channel and forwards it to the user.

* Text associated with the concerned button can be found in [texts.py](texts.py)
_____________________________________________________________________________________________________________________________________________________

# Trolls Functionality

1) Persistence Meme Club channel is regularly updated with ONLY meme material.
2) Every channel has a channel id, which works as a unique identifier.
3) Bot forwards a random meme from the channel in response to trolls button.
4) Bot can access only those messages that are sent to the channel after the bot was added to the channel and was given the right to access messages.
5) Each message in a Telegram channel/group has a message_id is associated with it.
6) We need to store and update a list of the message ids to access a random meme.
7) A free online SQL database is used for this purpose.
8) The SQL table is updated on every new image that is sent to the meme club channel.
9) Bot reads this table from the online database and picks a random message id.
10) The bot looks for the message associated with the id. In this case this message has been deleted, an erroe will be thrown.
11) We catch the exception and pick another random id. This process is repeated until we find a valid one. 
12) The meme with the selected message id is then forwarded to the user.

_____________________________________________________________________________________________________________________________________________________

# Keyword Recognition

The bot can recognise certain phrases and keywords, listed as follows:

Recognises (Hey, Hi, Hello) --> Replies with a greeting and command /start

Recognises ('Who are you', 'Who is this') --> Replies with "I am your bot" and instructions to restart the bot.

Recognises ('comdex' in user_message) --> Replies with link to the comdex product

Recognises a bunch of other keyowrds that are associated with queries that are to be answered. 
All those questions and their answers can be found in the comments in the [code file](texts.py).

____________________________________________________________________________________________________________________________________________________

# Messaage Forwarding and Repeating Memes and Stickers

To extract the sticker set we use the get_sticker_set() method which takes the name of your sticker set.
The sticker set that the bot currently uses is "Pbull".

1) Both these features are implemented using jobQueue. It allows to perform periodic functions with the bot.
2) It has a set of functions which include run_once(), run_daily(), run_repeating().
3) Apart from the function that it has to run, it takes two arguments of interval and first.
4) First refers to after how many SECONDS of deploying the function is supposed to run for the first time.
5) Interval refers to the number of SECONDS after which the bot will run the particular function again.
6) Datetime objects can also be passed as an argument if the function is supposed to run at a particular time.

Since we want to forward a message from the group only once, we use the run_once() function.

For Sending random memes and stickers, we use the run_repeating() function. Every 3 hours, the bot will send meme and sticker alternatively.

Find more details about the function at the [documentation](https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.jobqueue.html#telegram.ext.JobQueue)

_____________________________________________________________________________________________________________________________________________________
# Setup and Limitations

Bot is deployed on [Heroku](https://id.heroku.com/login) server with the app name 'persistence-test-bot' under its free tier.
The features of the same are as follows

1) The bot goes to idle 30 minutes after a message was last sent to it individually or in a group or channel the bot is a part of.
2) Once the bot is on sleep, it'll take an average of 15 seconds to reply to the first query. It'll reply instantaneously afterwards until it goes on sleep again.
3) We get 550 free hours of the service per month. These hours are not deducted when the bot is on sleep. 
4) These free hours can be increased to 1000 per month by verifying the account with a credit card. There is no charge for the same.

It is also linked with a database on [remotemysql.com](https://remotemysql.com), credentials of which can be found in the [bot.py](bot.py) code file.
1) It has a storage limit of 100 MB.
2) The database will be deleted if it is not updated in 30 days.

Use git to push files on heroku. The process has been explained [here](https://towardsdatascience.com/how-to-deploy-a-telegram-bot-using-heroku-for-free-9436f89575d2).

_______________________________________________________________________________________________________________________________________________________

# Helpful Links

[Deploy Bot on Heroku](https://towardsdatascience.com/how-to-deploy-a-telegram-bot-using-heroku-for-free-9436f89575d2)

[python-telegram-bot documentation](https://python-telegram-bot.readthedocs.io/en/stable/)

[Bot Examples](https://github.com/python-telegram-bot/python-telegram-bot)

