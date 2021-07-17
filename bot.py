import Constants as keys
import texts as sample_texts
from telegram.ext import *
from telegram import *
import Responses as R
import os
from datetime import datetime
import random
import mysql.connector as mysql


## An online SQL Database is linked with the bot. ##
## The SQL database is required for functioning of the 'Trolls' button. ##

## Credentials for the linked database.
HOST = "65.0.61.199:3306"    ## or link of the website that houses the database, if it shall be changed.

DATABASE = "tbot"     ## data-base name

USER = "melrose"         ## associated user

PASSWORD = "wQ$#V@b%M54Qg5WW"     ## password 


## connect to MySQL server
db_connection = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
mycursor = db_connection.cursor()

## Concerned Constants
PORT = int(os.environ.get('PORT', 5000))
API_KEY = '1636896963:AAHnCpeZAXrpSLWOgTaRkmoMjX5v9xFL5IU'      ## API Key of the Telegram Bot
CHANNEL_ID = -1001214674382    #Telegram Channel "PersistenceMemeClub" ID 
mybot = Bot(API_KEY)    ## Instance of the bot
ANNOUNCEMENT_CHANNEL_ID = -1001338629422  ## Persistence One official Announcement Channel ID
GROUP_CHAT_ID = -1001486887105  ## Test Group ID

## The 'TestList' table has been created in the associated SQL database. ##
## It is a single coloumn table that stores message id's of the memes that are sent in the Meme Channel on Telegram. ##
mycursor.execute("CREATE TABLE IF NOT EXISTS TestList (message_id int)")


## We fetch the integer column to local memory. Stored in 'message_ids_list'. ##
mycursor.execute("SELECT * FROM TestList")
message_ids_list = mycursor.fetchall()



##    Button Layout
##    _____________________________________________________
##    |          |                           |            |
##    |  About   |  Announcement             |   pStake   |
##    |__________|___________________________|____________|
##    |Website   |   Twitter   |   Discord   |   Blogs    |
##    |__________|_____________|_____________|____________|
##    |Wallet    |          Alerts           |   Trolls   |
##    |__________|___________________________|____________|



## The bot starts by sending the '/start' command (without the quotes). ##

def start_command(update, context):
    start_text = "Welcome to pBot! I'm here to serve the Persistence community.\n" \
                 "\n" \
                 "Please select an option from the menu below or type in your issue.\n" \
                 "I will try to redirect to something useful!"

    ## This command will launch the button menu for the user. ##
    ## The design can be changed by changing the matrix layout. ##
    
    reply_keyboard = [['About','Announcement','pStake'],['Website','Twitter','Discord','Blogs'] ,['Wallet', 'Alerts', 'Trolls']]
    update.message.reply_text(start_text,
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
                              )

# def Products_command(update, context):
#     update.message.reply_text("Visit https://persistence.one/products")
#
# def XPRT_command(update, context):
#     update.message.reply_text("Visit https://persistence.one/stakedrop")

def help_command(update, context):
    update.message.reply_text("HELPPPP MEEEE!!!")

def any_command(update, context):
    update.message.reply_text(sample_texts.about)



## 'Trolls' button and 'Token Release Schedule' Query reply with images and not texts.
##  Hence, they have been dealt with independently and not through sample_resonses function which deals with text replies.

def handle_message(update, context):

    if update.effective_chat.id == ANNOUNCEMENT_CHANNEL_ID:
        
        updater2 = Updater(API_KEY, use_context=True)
        dp2 = updater2.dispatcher

        def forward_announce(context: CallbackContext):
            try:
                Bot.forward_message(mybot, chat_id=GROUP_CHAT_ID,
                                    from_chat_id=ANNOUNCEMENT_CHANNEL_ID,
                                    message_id=update.channel_post.message_id)
            except:
                pass

        forwardQ = updater2.job_queue
        forwardQ.run_once(forward_announce, 5*3600)
        forwardQ.start()
        return

    if update.message != None:
        text = str(update.message.text).lower()

    ## Recognising a channel post
    if update.channel_post != None:
        text = ""
        
        if update.effective_chat.id == CHANNEL_ID:
            
            try:
                db_connection = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
                mycursor = db_connection.cursor()
                id_to_add = update.channel_post.message_id
                mycursor.execute("INSERT INTO TestList (message_id) VALUES (%s)", (id_to_add,))
                db_connection.commit()
            except:
                print("Couldn't update file")

    ## Token Release Schedule Query Handling
    if 'token' in text and 'release' in text and 'schedule' in text:
        photo_id = sample_texts.token_release_schedule_image_id
        try:
            mybot.sendPhoto(update.message.chat.id, photo=photo_id)
        except Exception as e:
            update.message.reply_text("Error --> " + str(e))

    ## Troll Button Handling
    if text == 'trolls':
        try:
            db_connection = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
            mycursor = db_connection.cursor()
            mycursor.execute("SELECT * FROM TestList")
            message_ids_list = mycursor.fetchall()
            
            boolean = True
            while boolean:
                try:
                    num = random.randint(0, (len(message_ids_list)-1))
                    Bot.forward_message(mybot, chat_id=update.message.chat.id,
                                from_chat_id=CHANNEL_ID,
                                message_id=message_ids_list[num][0])
                    boolean = False
                except:
                    boolean = True
            
        except Exception as e:
            update.message.reply_text("Error! --> " + str(e))

    ## Text Response Handling
    else:
        text = str(update.message.text).lower()
        response = sample_responses(text)
        if(len(response) != 0):
            update.message.reply_text(response)
        #update.message.reply_text(response)



def sample_responses(input_text):
    user_message = str(input_text)
    user_message = user_message.lower()
    greet_text = "Hello! This is your Persistence One Bot.\n" \
                 "Please click /start to get started."

    ## Replying to standard greetings
    
    if user_message in ("hi", "hello", "sup", "sup?", "hey"):
        return greet_text

    if user_message in ("who is this", "who are you", "who are you?"):
        return greet_text

    if user_message in ('time', 'time?'):
        now = datetime.now()
        date_time = now.strftime('%d/%m/%y, %H:%M:%S')
        return str(date_time)


    ## QUERY HANDLING

    if 'stakedrop' in user_message:
        return sample_texts.stakedrop_text

    if 'phrasekey' in user_message and 'keystore' in user_message:
        return sample_texts.phrasekey_keystore_text

    if 'roadmap' in user_message:
        return sample_texts.roadmap_text

    if 'exchange' in user_message or 'listing' in user_message:
        return sample_texts.exchange_xprt_text

    if 'wallet' in user_message and 'xprt' in user_message:
        return sample_texts.wallet_xprt_text

    if 'pstake' in user_message and ('launch' in user_message or 'live' in user_message):
        return sample_texts.pstake_launch_text

    if 'unbound' in user_message and 'unstak' in user_message:
        return sample_texts.unbounding_untsaking_text

    if ('xprt' in user_message and 'stak' in user_message) or ('reward' in user_message and 'delegat' in user_message):
        return sample_texts.xprt_staking_text

    if 'hardware' in user_message and 'wallet' in user_message:
        return sample_texts.hardware_wallet_text

    if ('max' in user_message or 'current' in user_message) and 'supply' in user_message:
        return sample_texts.max_current_supply_text
    
    
    #Checking user message for specific keywords
    if user_message == 'wallet' or user_message == 'wallets':
        wallet_text = "For issues and information regarding the wallet service\n" \
                      "Please visit\n" \
                      "https://wallet.persistence.one/"
        return wallet_text

    if 'comdex' in user_message:
        comdex_text = "For issues and information regarding the comdex service\n" \
                      "Please visit: comdex.one"
        return comdex_text

        
    #Button Responses

    #NEW RESPONSES
    if user_message == 'about':
        return sample_texts.about_text
    
    if user_message == 'announcement':
        return sample_texts.announcement_text

    if user_message == 'pstake':
        return sample_texts.pstake_text

    if user_message == 'website':
        return sample_texts.website_text

    if user_message == 'twitter':
        return sample_texts.twitter_text

    if user_message == 'discord':
        return sample_texts.discord_text

    if user_message == 'blogs':
        return sample_texts.blogs_text

    if user_message == 'wallet':
        wallet_text = "For issues and information regarding the wallet service\n" \
                      "Please visit\n" \
                      "https://wallet.persistence.one/"
        return wallet_text

    if user_message == 'alerts':
        return sample_texts.alerts_text

####### REDDIT PRAW VERSION  #######

##    if user_message == 'trolls':
##        #return 'Feature under development. Aim is to return a random crypto-related meme.'
##        try:
##            reddit = praw.Reddit(client_id='******',
##                                 client_secret='******',
##                                 #password='******',
##                                 username='******',
##                                 user_agent='******')
##            subreddit = reddit.subreddit('cryptocurrencymemes')
##            meme = subreddit.random()
##            #print(type(meme))
##            #print(type(meme.url))
##            # update.message.reply_text(meme.url)
##            return meme.url
##        except Exception as e:
##            print(e)
##            return 'Error! Please try a different command :)'




    
    # PREVIOUS RESPONSES
##    if user_message == 'products':
##        return "Visit https://persistence.one/products"
##
##    if user_message == 'earn $xprt':
##        xprt_text = "To earn $ XPRT visit here:\n" \
##                    "https://persistence.one/stakedrop"
##        return xprt_text
##
##    if user_message == 'warning':
##        warning_text = "Beware of scammers!\n" \
##                       "Check with the following usernames\n" \
##                       "@PersistenceOneChat and @PersistenceOne"
##        return warning_text
##
##    if user_message == 'roadmap':
##        roadmap_text = "Our roadmap can be accessed here:\n" \
##                       "https://persistence.one/roadmap"
##        return roadmap_text
##
##    if user_message == 'token sale':
##        tokenSale_text = 'Private Sale has ended\n' \
##                         'Public Sale - Due for Q1 2021\n' \
##                         'Please access the Public Sale interest form here:\n' \
##                         'https://t.me/PersistenceOne/230'
##        return tokenSale_text

    return ''
    #Unhandled Cases
    #standard = 'Sorry I don\'t understand.\n' \
    #           'Please type again! OR\n' \
    #           'Please type /start to restart the bot.'
    #return standard

def repeat_sticker(context: CallbackContext):
    pbull_sticker_set = mybot.get_sticker_set("Pbull")
    pbull_stickers = pbull_sticker_set.stickers
    rand = random.randint(0, len(pbull_stickers)-1)
    try:
        mybot.sendSticker(GROUP_CHAT_ID, pbull_stickers[rand])
    except:
        pass

def repeat_meme(context: CallbackContext):
    try:
        db_connection = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        mycursor = db_connection.cursor()
        mycursor.execute("SELECT * FROM TestList")
        message_ids_list = mycursor.fetchall()
        
        boolean = True
        while boolean:
            try:
                num = random.randint(0, (len(message_ids_list)-1))
                Bot.forward_message(mybot, chat_id=GROUP_CHAT_ID,
                            from_chat_id=CHANNEL_ID,
                            message_id=message_ids_list[num][0])
                boolean = False
            except:
                boolean = True
        
    except Exception as e:
        pass



def main():
    updater = Updater(API_KEY, use_context=True)
    dp = updater.dispatcher

    jobQ = updater.job_queue
    jobQ.run_repeating(repeat_sticker, interval=6*3600, first=20)

    jobQ2 = updater.job_queue
    jobQ2.run_repeating(repeat_meme, interval=6*3600, first=3*3600)
    
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("any", any_command))
    # dp.add_handler(CommandHandler("XPRT", XPRT_command))
    # dp.add_handler(CommandHandler("Products", Products_command))

    dp.add_handler(MessageHandler(Filters.all, handle_message))

    #POLLING
    #updater.start_polling()

    #WEBHOOK
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=API_KEY)
    updater.bot.setWebhook('https://persistence-test-bot.herokuapp.com/' + API_KEY)
    
    updater.idle()

if __name__ == '__main__':
    main()
