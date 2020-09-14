#insalling libraries
!pip install python-telegram-bot
!pip install adafruit-io



#adafruit part
X = os.getenv('X')                     # ADAFRUIT_IO_USERNAME
Y = os.getenv('Y')                     # ADAFRUIT_IO_KEY

from Adafruit_IO import Client, Feed
aio = Client(X,Y)



#telegram part
from telegram.ext import Updater,CommandHandler, MessageHandler, Filters  

import requests  # Getting the data from the cloud

def get_url():
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents ['url']
    return url


def lighton(bot,update):
    data = aio.send('lightbot', 1)
    rdata = aio.receive('lightbot').value
    chat_id = update.message.chat_id
    bot.send_message(chat_id,text='Light is On')
    url = get_url()
    bot.send_photo(chat_id,photo=url)
    bot.send_message(chat_id,text='Request processed')


def lightoff(bot,update):
    data = aio.send('lightbot', 0)
    rdata = aio.receive('lightbot').value
    chat_id = update.message.chat_id
    bot.send_message(chat_id,text='Light is Off')
    url = get_url()
    bot.send_photo(chat_id,photo=url)
    bot.send_message(chat_id,text='Request processed')


def chooser(bot,update):
          chat_id = update.message.chat_id
            
          a = update.message.text

          data = aio.receive_previous('lightbot')

          if a == "Light on" or a =="Light ON" or a =="Light On" or a == "LIGHT ON" or a =="light on" and data == 0:
                { 
                        lighton(bot,update)
                }
          elif a == "Light off" or a =="Light OFF" or a =="Light Off" or a == "LIGHT OFF" or a =="light off" and data == 1:
                {
                        lightoff(bot,update)
                }
          else:
                {
                        bot.send_message(chat_id,text='Invalid Text')
                }



u = Updater('1171508830:AAHdsf3BzMRpIHVpGOdh5XGFYChRSTNGwOo')
dp = u.dispatcher
dp.add_handler(MessageHandler(Filters.text, chooser))
u.start_polling()
u.idle()
