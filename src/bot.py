from typing import Optional, Dict
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, InlineQueryHandler, \
    MessageHandler, filters
from google.cloud import firestore
import logging
import sys

from app_config import TELEGRAM_BOT_TOKEN, FIRESTORE_CREDENTIAL_PATH, FIRESTORE_PROJECT_ID

# Define constants for states
NOT_STARTED = 1
RECEIVED_MERCHANT_COMMAND = 2
USER_NOT_REGISTERED = 3
USER_REGISTERED = 4

# Initialize Firestore
db = firestore.Client.from_service_account_json(
    json_credentials_path=FIRESTORE_CREDENTIAL_PATH,
    project=FIRESTORE_PROJECT_ID
)

# State management dictionary
user_states: Dict[int, int] = {}

# Configure logging
logging.basicConfig(level=logging.INFO, filename="../logs/telegram_bot.log", filemode="w")
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))  # defaults to sys.stderr


# Handle start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user_states[user_id] = NOT_STARTED
    await update.message.reply_text('Bot started. Use the inline command to proceed.')
    logger.info(f"User {user_id} started the bot.")


# Handle inline command
async def inline_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f"inline command received {update.message.text}")
    query = update.inline_query.query.split()
    if len(query) != 2:
        return

    user_id = update.inline_query.from_user.id
    bot_name, merchant_name = query

    if bot_name != 'heymax_shop_bot':
        return

    user_data = get_user_data(user_id)
    if not user_data:
        user_states[user_id] = USER_NOT_REGISTERED
        await context.bot.send_message(chat_id=user_id, text="Please provide your email address to register.")
        logger.info(f"User {user_id} is not registered. Asking for email address.")
    else:
        user_states[user_id] = USER_REGISTERED
        await send_affiliate_link(user_id, merchant_name, context)


# Handle user registration
async def register_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f"Register user received {update.message.text}")
    user_id = update.message.from_user.id
    email = update.message.text.strip()

    heymax_user_id = get_heymax_user_id_by_email(email)
    if not heymax_user_id:
        await update.message.reply_text('Email not found. Please provide a valid email address.')
        logger.warning(f"Email {email} not found in heymax user profile.")
        return

    save_user_data(user_id, email, heymax_user_id)
    user_states[user_id] = USER_REGISTERED
    await update.message.reply_text('Registration successful! Now you can use the inline command.')
    logger.info(f"User {user_id} registered with email {email}.")


# Send affiliate link
async def send_affiliate_link(user_id: int, merchant_name: str, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_data = get_user_data(user_id)
    heymax_user_id = user_data['heymax_user_id']

    affiliate_link_data = get_affiliate_link_data(merchant_name)
    if not affiliate_link_data:
        await context.bot.send_message(chat_id=user_id, text="Merchant not found.")
        logger.warning(f"Merchant {merchant_name} not found in affiliate links.")
        return

    tracking_link = generate_tracking_link(affiliate_link_data, heymax_user_id)
    keyboard = [[InlineKeyboardButton("Your Unique Shop with Max Link", url=tracking_link)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=user_id, text="Here is your unique affiliate link:",
                                   reply_markup=reply_markup)
    logger.info(f"Sent affiliate link to user {user_id} for merchant {merchant_name}.")


# Generate tracking link based on platform
def generate_tracking_link(affiliate_data: Dict[str, str], user_id: str) -> str:
    tracking_link = affiliate_data['trackingLink']
    source_platform = affiliate_data['sourcePlatform']

    if "{USER_ID}" in tracking_link:
        return tracking_link.replace("{USER_ID}", user_id).replace("{OFFER_UUID}", affiliate_data['id'])

    platform_links = {
        "IMPACT": f"{tracking_link}?subid1={user_id}",
        "INVOLVE_ASIA": f"{tracking_link}?aff_sub={user_id}",
        "COMMISSION_FACTORY": f"{tracking_link}&UniqueId={user_id}",
        "OPTIMISE": f"{tracking_link}&UID={user_id}",
        "CJ": f"{tracking_link}?sid={user_id}",
        "RAKUTEN": f"{tracking_link}&u1={user_id}",
        "PARTNERIZE": f"{tracking_link}/pubref:{user_id}",
        "AWIN": f"{tracking_link}&clickref={user_id}"
    }

    return platform_links.get(source_platform, tracking_link)


# Database interaction functions
def get_user_data(user_id: int) -> Optional[Dict[str, str]]:
    doc = db.collection('user_profile_telegram').document(str(user_id)).get()
    return doc.to_dict() if doc.exists else None


def save_user_data(user_id: int, email: str, heymax_user_id: str) -> None:
    db.collection('user_profile_telegram').document(str(user_id)).set({
        'telegram_user_id': user_id,
        'email': email,
        'heymax_user_id': heymax_user_id
    })


def get_heymax_user_id_by_email(email: str) -> Optional[str]:
    docs = db.collection('user_profile_telegram').where('email', '==', email).get()
    return docs[0].get('heymax_user_id') if docs else None


def get_affiliate_link_data(merchant_name: str) -> Optional[Dict[str, str]]:
    doc = db.collection('affiliate_links_telegram').document(merchant_name).get()
    return doc.to_dict() if doc.exists else None


# Main function to start the bot
def main() -> None:
    logger.info(f"Starting Shop with heymax Telegram bot")
    if TELEGRAM_BOT_TOKEN:
        application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    else:
        logger.warning(f"TELEGRAM_BOT_TOKEN does not exist. Please provide a valid Telegram bot token.")

    start_handler = CommandHandler('start', start)
    inline_handler = InlineQueryHandler(inline_command)
    registration_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, register_user)

    application.add_handler(start_handler)
    application.add_handler(inline_handler)
    application.add_handler(registration_handler)

    application.run_polling()


if __name__ == '__main__':
    main()
