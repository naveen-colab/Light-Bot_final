!pip install python-telegram-bot
!pip install adafruit-io


#adafruit part

X = os.getenv('X')                     # ADAFRUIT_IO_USERNAME
Y = os.getenv('Y')"    # ADAFRUIT_IO_KEY

from Adafruit_IO import Client, Feed
aio = Client(X,Y)


#logging exception handler

import logging
import os

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  
                    level=logging.INFO)
logger = logging.getLogger(__name__)



from telegram.ext import Updater, CommandHandler,MessageHandler, Filters 

def lightoff(bot,update):
    data = aio.send('lightbot', 0)
    rdata = aio.receive('lightbot').value
    chat_id = bot.message.chat_id
    bot.message.reply_text('Request processing')
    update.bot.sendPhoto(chat_id=chat_id, photo="https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcQ8jpdHR_pFaoP2Vudl7k-46mSK7I3shuCvFw&usqp=CAU", caption="Light off")
    
def lighton(bot,update):
    data = aio.send('lightbot', 1)
    rdata = aio.receive('lightbot').value
    chat_id = bot.message.chat_id
    bot.message.reply_text('Request Processing')
    update.bot.sendPhoto(chat_id=chat_id, photo="https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcRgKuBghXuR_IjPXnRu9o2znn0O_avidTs-ig&usqp=CAU", caption="Light on")
    
def chooser(bot,update):
          chat_id = bot.message.chat_id
            
          a = bot.message.text

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
                        bot.message.reply_text('Invalid Text')
                }

def main():
  BOT_TOKEN= os.getenv('BOT_TOKEN')
  u = Updater(BOT_TOKEN, use_context=True)
  dp = u.dispatcher
  dp.add_handler(MessageHandler(Filters.text, chooser))
  u.start_polling()
  u.idle()
  
if __name__ == '__main__':
    main()
