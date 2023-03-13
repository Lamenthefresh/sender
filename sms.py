import requests
import config


# Fonction pour envoyer des SMS via l'API SMS
def send_sms(phone, message):
    payload = {'api_key': config.SMS_API_KEY,
               'api_secret': config.SMS_API_SECRET,
               'from': config.SMS_API_FROM,
               'to': phone,
               'text': message}
    try:
        response = requests.post(config.SMS_API_URL, data=payload)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        return False
