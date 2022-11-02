from django.core.management.base import BaseCommand
from django.conf import settings
from telegram import Bot 
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import Filters 
from telegram.ext import MessageHandler
from telegram.ext import Updater
from telegram.utils.request import Request
from tb.models import Profile

#TG_API_URL = "https://telegg.ru/orig/bot" 
TOKEN = '5723230723:AAElREEDY7ug4ex9GsHf_0QJUcD6WWUS3NQ'

def log_errors(f):

    def inner(*args,**kwargs):
        try:
            return f(*args,**kwargs)
        except Exception as e : 
            error_message = f'Error occured : {e}'
            print(error_message)
            raise e 

    return inner

@log_errors
def do_echo(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    text = update.message.text

    p, _ = Profile.objects.get_or_create(
        external_id = chat_id, 
        defaults = {
            'name': update.message.from_user.username ,
        }
    )

    reply_text = " Your ID is = {}\n\n{}".format(chat_id , text)
    update.message.reply_text(
        text = reply_text,
    )

class Command(BaseCommand):
    help = 'Telegram-bot'

    def handle(self, *args, **options):
        #1-- successful connection
        request = Request(
            connect_timeout = 0.5,
            read_timeout = 1.0  ,
        )
        bot = Bot( 
            request = request,
            token = TOKEN,
            #base_url = TG_API_URL 
        )
        print(bot.get_me())

        #2- handlers
        updater = Updater(
            bot = bot,
            use_context = True
        )
        message_handler = MessageHandler(Filters.text, do_echo)
        updater.dispatcher.add_handler(message_handler)

        #3 - endless processing of incoming messages
        updater.start_polling()
        updater.idle()