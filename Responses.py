from datetime import datetime

def sample_responses(input_text):
    user_message = str(input_text)
    user_message = user_message.lower()
    greet_text = "Hello! This is your Persistence One Bot.\n" \
                 "Please click /start to get started."

    ## Replying to standard greetings and questions
    if user_message in ("hi", "hello", "sup", "sup?", "hey"):
        return greet_text

    if user_message in ("who is this", "who are you", "who are you?"):
        return greet_text

    if user_message in ('time', 'time?'):
        now = datetime.now()
        date_time = now.strftime('%d/%m/%y, %H:%M:%S')
        return str(date_time)

    #Checking user message for specific keywords
    if 'wallet' in user_message:
        wallet_text = "For issues and information regarding the wallet service\n" \
                      "Please visit\n" \
                      "https://wallet.persistence.one/"
        return wallet_text

    if 'comdex' in user_message:
        comdex_text = "For issues and information regarding the comdex service\n" \
                      "Please visit\n" \
                      "https://comdex.sg/"
        return comdex_text

    #Button Responses
    if user_message == 'products':
        return "Visit https://persistence.one/products"

    if user_message == 'earn $xprt':
        xprt_text = "To earn $ XPRT visit here:\n" \
                    "https://persistence.one/stakedrop"
        return xprt_text

    if user_message == 'warning':
        warning_text = "Beware of scammers!\n" \
                       "Check with the following usernames\n" \
                       "@PersistenceOneChat and @PersistenceOne"
        return warning_text

    if user_message == 'roadmap':
        roadmap_text = "Our roadmap can be accessed here:\n" \
                       "https://persistence.one/roadmap"
        return roadmap_text

    if user_message == 'token sale':
        tokenSale_text = 'Private Sale has ended\n' \
                         'Public Sale - Due for Q1 2021\n' \
                         'Please access the Public Sale interest form here:\n' \
                         'https://t.me/PersistenceOne/230'
        return tokenSale_text


    #Unhandled Cases
    standard = 'Sorry I don\'t understand.\n' \
               'Please type again! OR\n' \
               'Please type /start to restart the bot.'
    return standard
