import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from config import TELEGRAM_TOKEN

# Initialisation du module de logging
logger = logging.getLogger(__name__)

# Fonction pour gérer la commande /start
def start(update, context):
    update.message.reply_text('Bienvenue dans l\'application Sender!')

# Fonction pour gérer les messages entrants
def echo(update, context):
    update.message.reply_text('Désolé, je ne peux pas traiter les messages. Veuillez utiliser les commandes disponibles.')

# Fonction pour gérer la commande /help
def help(update, context):
    update.message.reply_text('Voici les commandes disponibles:\n/start - Pour démarrer l\'application\n/help - Pour afficher l\'aide')

# Fonction pour envoyer un SMS
def send_sms(update, context):
    # Récupération des informations de l'utilisateur
    chat_id = update.message.chat_id
    phone_numbers = context.args[0]
    message = " ".join(context.args[1:])
    
    # Envoi du SMS
    try:
        # Boucle pour envoyer le SMS à chaque numéro de téléphone
        for phone_number in phone_numbers.split(","):
            # Envoi du SMS
            # TODO: Compléter cette fonction pour envoyer réellement le SMS
            logger.info(f"SMS envoyé à {phone_number}: {message}")
            update.message.reply_text(f"SMS envoyé à {phone_number} avec succès.")
            time.sleep(7) # Attendre 7 secondes pour éviter le spam
    except Exception as e:
        logger.error(f"Erreur lors de l'envoi du SMS: {e}")
        update.message.reply_text("Une erreur est survenue lors de l'envoi du SMS.")

# Fonction pour gérer les erreurs
def error(update, context):
    logger.warning(f"Update {update} caused error {context.error}")

# Fonction pour initialiser le bot Telegram
def init_telegram_bot():
    # Initialisation du bot Telegram
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)

    # Récupération du dispatcher pour enregistrer les commandes et les messages entrants
    dp = updater.dispatcher

    # Enregistrement des commandes et des messages entrants
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("sms", send_sms))
    dp.add_handler(MessageHandler(Filters.text, echo))

    # Enregistrement de la fonction pour gérer les erreurs
    dp.add_error_handler(error)

    # Démarrage du bot Telegram
    updater.start_polling()

    # Mise en attente de l'arrêt du bot
    updater.idle()
