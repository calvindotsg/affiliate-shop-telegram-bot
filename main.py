# main.py
import firebase_admin
from firebase_admin import credentials, firestore
import telebot
from bot import AffiliateBot

def main():
    # Initialize Firestore with your service account key.
    cred = credentials.Certificate("path/to/serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    # Initialize the Telegram Bot with your API token.
    API_TOKEN = "YOUR_TELEGRAM_BOT_API_TOKEN"
    bot = telebot.TeleBot(API_TOKEN)

    # Create an instance of the AffiliateBot and start it.
    affiliate_bot = AffiliateBot(bot, db)
    affiliate_bot.start()

if __name__ == "__main__":
    main()