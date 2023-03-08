import logging
import os

from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, filters

a = 1

IP = range(1)

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

    reply_keyboard = [['/cancel']]
    update.message.reply_text(
        '¿Cuál es la dirección IP de su víctima? (Escriba "/cancel" para cancelar la petición)',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return IP

def set_ip(update, context):

    ip = update.message.text

    # Hacemos lo que necesites con la dirección IP
    # ...

    return ConversationHandler.END

def cancel(update, context):

    update.message.reply_text('Operación cancelada')

    return ConversationHandler.END

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('attack', attack)],
    states={
        IP: [MessageHandler(filters.text & ~filters.command, set_ip)]
    },
    fallbacks=[MessageHandler(filters.regex('^Cancelar$'), cancel)]
)

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
