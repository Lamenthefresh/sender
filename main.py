import logging
import config
import sms
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Initialisation du journal
logging.basicConfig(filename='logs/sender.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


# Fonction de démarrage du bot
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Bonjour! Envoyez /sms pour envoyer un SMS.")


# Fonction pour envoyer des SMS
def send_sms(update, context):
    # Demander le numéro de téléphone et le message à l'utilisateur
    context.bot.send_message(chat_id=update.effective_chat.id, text="Entrez le numéro de téléphone:")
    phone = context.bot.get_updates()[-1].message.text
    context.bot.send_message(chat_id=update.effective_chat.id, text="Entrez le message:")
    message = context.bot.get_updates()[-1].message.text
    
    # Envoyer le SMS en utilisant l'API SMS
    result = sms.send_sms(phone, message)
    
    # Envoyer un message de confirmation ou d'erreur à l'utilisateur
    if result:
        context.bot.send_message(chat_id=update.effective_chat.id, text="SMS envoyé avec succès!")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Une erreur est survenue lors de l'envoi du SMS.")


# Fonction pour gérer les erreurs
def error(update, context):
    logging.warning('Update "%s" caused error "%s"', update, context.error)


# Configuration et lancement du bot
if __name__ == '__main__':
    updater = Updater(token=config.TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Ajouter les gestionnaires de commandes
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("sms", send_sms))

    # Ajouter le gestionnaire de messages
    dp.add_handler(MessageHandler(Filters.text, send_sms))

    # Gérer les erreurs
    dp.add_error_handler(error)

    # Lancer le bot
    updater.start_polling()
    updater.idle()
