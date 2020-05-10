from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import Update, ParseMode
import requests
import re
import logging
import random 
import metallum

# more of the dog thing
def get_url():
    contents = requests.get('https://random.dog/woof.json').json()    
    url = contents['url']
    return url

# the dog thing.
def bop(bot, update):
    url = get_url()
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=url)

#dice math for roller
def dice(count, side):
    score_list = []
    x = 1
    limit_msg = ''

    # int conversion just in case...
    sidez = int(side)
    # limit to sides of dice
    if sidez > 1000:
        sidez = 1000
        limit_msg = "\nMax sides to a dice limited to 1000 and even that is too much. stop being an idiot."
    countz = int(count)
    # dice throw loop
    while x <= countz:
        throw_num = random.randint(1,sidez)
        score_list.append(throw_num)
        x += 1
    # sum the score
    dice_sum = sum(score_list)

    return dice_sum, score_list, limit_msg 

#testing if dice count and sides are integers and can be used in calculations
def integ_test(count, side):    
    try:
        float(count)
    except ValueError:
        count_is_int = False
    else:
        count_is_int = float(count).is_integer()

    try:
        float(side)
    except ValueError:
        sides_is_int = False
    else:
        sides_is_int = float(side).is_integer()       

    # final verdict   
    if count_is_int and sides_is_int:
        return True
    else:
        return False


# the roll command function 
def lol(bot, update, args):

    # most of these strings were just for testing.
    answerstring = 'answer '
    sides = ' sides:non '
    d_count = ' dcount:non '
    errormesg = 'follow the format.\nFor example "/lol 4d6"'
    #take args 0 if there is any
    if len(args) >= 1:
        parse_this = args[0]

        # searching for that all important d
        d_loc = parse_this.find("d")
        
        #if d is at 0, no number of dice given. = 1 dice
        if d_loc == 0:
            d_count = 1
            # the numbers after the d
            sides = parse_this[int(d_loc)+1:]
            answerstring = 'you rolled '
            # integer check
            math_time = integ_test(d_count, sides)

            # if integer checks came back true, it is indeed math time
            if math_time:
                # dice() will do the math and also return possible message
                total, d_list, lim_msg = dice(d_count, sides)
                #compiling final message
                shitload = d_count + ' x ' + sides + ' sided dice for a total of ' + str(total) + '\ndice: ' + str(d_list)
                answerstring = answerstring + shitload + lim_msg
            else:
                # integer(s) came out false
                answerstring = errormesg
        
        elif d_loc == -1:
            #the d not found
            answerstring = errormesg
        elif d_loc > 0 and d_loc <= 2:
            #sensible amount of dice. time to parse the numbers from both sides
            d_count = parse_this[:int(d_loc)]
            sides = parse_this[int(d_loc)+1:]
            answerstring = 'you rolled '
            # integer check. this and all after this repetition from the 1d scenario.
            # could probably have easily avoided this repetition but will fix later.
            math_time = integ_test(d_count, sides)
            
            if math_time:
                totale, d_list, lim_msg = dice(d_count, sides)
                shitload = d_count + ' x ' + sides + ' sided dice for a total of ' + str(totale) + '\ndice: ' + str(d_list)
                answerstring = answerstring + shitload + lim_msg
            else:
                answerstring = errormesg

        else:
            #too many dice bro
            answerstring = 'the max amount of dice has been limited to 99. try again please'

    else:
        answerstring = errormesg
    # update chat id and send the final message
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text=answerstring)


def maa(bot, update, args):

    parse_band = 'pantera'
    wanted = 'no'
    if len(args) >= 1:
        parse_band = args[0]
        parse_band = parse_band.replace("_"," ")
    
    if len(args) >= 2:
        wanted = args[1]
    # add args1 and 2 to make more detailed searches...
    bands = metallum.band_search(parse_band)
    # for now just take first band from options...
    band_name = bands[0].name
    band = bands[0].get() 
    band_albums = band.albums

    album_info = '\nAdd "albums" as argument 2 to get list of albums'
    if wanted == 'albums':
        album_info = '\n'.join(map(str, band_albums))

    band_info = ' '.join(map(str, bands[0]))


    infostring = band_info + "\n" + album_info

    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text=infostring)


# non important function for now
def start(bot, update, context):
    aaa = 'starttooo'
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text=aaa)

# trying out a basic active echo
def echo(update, context):
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id=chat_id, text=update.message.text)



def main():
    with open('token.txt', 'r') as file:
        token_text = file.read()
    updater = Updater(token_text)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('bop',bop))

    dp.add_handler(CommandHandler('lol', lol, pass_args=True))

    dp.add_handler(CommandHandler('maa', maa, pass_args=True))

    dp.add_handler(CommandHandler('start', start))

    dp.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()