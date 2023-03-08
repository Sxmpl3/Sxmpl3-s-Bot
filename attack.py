import logging
import os

a = 1

from telegram.ext import Updater, CommandHandler, MessageHandler, filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def start(update, context):
    """Comando /start"""

    update.message.reply_text('Hola pringao, usa /help para ver los comandos disponibles')


def help(update, context):
    """Comando /help"""

    update.message.reply_text('Los comandos disponibles son los siguientes:')
    update.message.reply_text('')
    update.message.reply_text('/start')
    update.message.reply_text('/help')
    update.message.reply_text('/attack')

def attack(update, context):
    """Comando /attack"""

    update.message.reply_text('Introduzca la dirección IP de su victima...')

    while a > 10:
        
        print("Esto es una prueba")

def main():
    """Se inicia el bot"""

    updater = Updater("6140799429:AAH3UwOcl4GlqqIy0oRKrTjbEfUAWWCicgU", use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("attack", attack))
    updater.start_polling()

    updater.idle()



if __name__ == '__main__':
    main()

