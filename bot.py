# bot.py
from enum import Enum, auto
import telebot
from telebot import types
from utils import generate_tracking_link

class UserState(Enum):
    NOT_STARTED = auto()
    RECEIVED_COMMAND = auto()
    NOT_REGISTERED = auto()
    REGISTERED = auto()

class AffiliateBot:
    def __init__(self, bot: telebot.TeleBot, db):
        """
        Initialize the AffiliateBot with a Telegram bot instance and Firestore database client.

        Parameters:
            bot (telebot.TeleBot): The Telegram bot instance.
            db: The Firestore database client.
        """
        self.bot = bot
        self.db = db
        self.user_states = {}  # Maps Telegram user_id to UserState

    def start(self):
        """
        Set up command and callback handlers and start polling for messages.
        """
        @self.bot.message_handler(commands=['shop'])
        def handle_shop_command(message):
            user_id = message.from_user.id
            command_parts = message.text.split()
            if len(command_parts) != 2:
                self.bot.reply_to(message, "Invalid command format. Use /shop <MerchantName>")
                return

            merchant_name = command_parts[1]
            self.user_states[user_id] = UserState.RECEIVED_COMMAND

            if self.is_user_registered(user_id):
                self.user_states[user_id] = UserState.REGISTERED
                self.send_affiliate_link(user_id, merchant_name, message)
            else:
                self.user_states[user_id] = UserState.NOT_REGISTERED
                self.request_user_email(user_id, message)

        @self.bot.callback_query_handler(func=lambda call: True)
        def handle_callback_query(call):
            user_id = call.from_user.id
            if call.data == "request_email":
                self.request_user_email(user_id, call.message)
            elif call.data.startswith("affiliate_link_"):
                # Expect callback data in the format "affiliate_link_<MerchantName>"
                parts = call.data.split("_", 2)
                if len(parts) == 3:
                    merchant_name = parts[2]
                    self.send_affiliate_link(user_id, merchant_name, call.message)

        self.bot.polling()

    def is_user_registered(self, user_id: int) -> bool:
        """
        Check if the user is registered in the 'user_profile_telegram' collection.

        Parameters:
            user_id (int): Telegram user ID.

        Returns:
            bool: True if the user exists; otherwise, False.
        """
        doc_ref = self.db.collection('user_profile_telegram').document(str(user_id))
        doc = doc_ref.get()
        return doc.exists

    def request_user_email(self, user_id: int, message):
        """
        Prompt the user to provide their registered email address.

        Parameters:
            user_id (int): Telegram user ID.
            message: The original message triggering the request.
        """
        self.bot.send_message(user_id, "Please provide your registered email address:")
        self.bot.register_next_step_handler(message, self.handle_user_email)

    def handle_user_email(self, message):
        """
        Handle the email provided by the user for registration.

        Parameters:
            message: The message containing the user's email.
        """
        user_id = message.from_user.id
        email = message.text.strip()
        affiliate_user_id = self.lookup_affiliate_user_id(email)
        if affiliate_user_id:
            self.register_user(user_id, email, affiliate_user_id)
            self.user_states[user_id] = UserState.REGISTERED
            self.bot.send_message(user_id, "Registration successful.")
        else:
            self.bot.send_message(user_id, "Invalid email address. Please try again.")
            self.request_user_email(user_id, message)

    def lookup_affiliate_user_id(self, email: str) -> str:
        """
        Look up the unique affiliate user identifier based on the email.

        Parameters:
            email (str): The user's email address.

        Returns:
            str: The unique affiliate user ID if found; otherwise, None.
        """
        user_profile_ref = self.db.collection('user_profile').where('email', '==', email).limit(1)
        docs = user_profile_ref.stream()
        for doc in docs:
            return doc.id
        return None

    def register_user(self, user_id: int, email: str, affiliate_user_id: str):
        """
        Register the user by storing their Telegram and affiliate user IDs along with their email.

        Parameters:
            user_id (int): Telegram user ID.
            email (str): User's email address.
            affiliate_user_id (str): Unique affiliate user identifier.
        """
        self.db.collection('user_profile_telegram').document(str(user_id)).set({
            'telegram_user_id': user_id,
            'email': email,
            'affiliate_user_id': affiliate_user_id
        })

    def get_affiliate_user_id(self, user_id: int) -> str:
        """
        Retrieve the affiliate user ID associated with the given Telegram user ID.

        Parameters:
            user_id (int): Telegram user ID.

        Returns:
            str: The affiliate user ID if registered; otherwise, None.
        """
        doc = self.db.collection('user_profile_telegram').document(str(user_id)).get()
        if doc.exists:
            return doc.to_dict().get('affiliate_user_id')
        return None

    def send_affiliate_link(self, user_id: int, merchant_name: str, message):
        """
        Generate and send a personalized affiliate tracking link to the user.

        Parameters:
            user_id (int): Telegram user ID.
            merchant_name (str): The merchant name provided in the command.
            message: The message context for replying.
        """
        try:
            affiliate_link = self.generate_affiliate_link(user_id, merchant_name)
            markup = types.InlineKeyboardMarkup()
            button = types.InlineKeyboardButton("Your Unique Shop Link", url=affiliate_link)
            markup.add(button)
            self.bot.send_message(message.chat.id, "Click the button below to shop:", reply_markup=markup)
        except Exception as e:
            self.bot.send_message(message.chat.id, f"Error generating affiliate link: {str(e)}")

    def generate_affiliate_link(self, user_id: int, merchant_name: str) -> str:
        """
        Generate the affiliate tracking link based on the user and merchant information.

        Parameters:
            user_id (int): Telegram user ID.
            merchant_name (str): The merchant name provided by the user.

        Returns:
            str: The personalized affiliate tracking link.
        """
        # For demonstration purposes, affiliate_data is hard-coded.
        # In a real application, this data should be fetched from a database or configuration.
        affiliate_data = {
            'trackingLink': 'https://example.com',
            'sourcePlatform': 'IMPACT',
            'id': 'offer_uuid'
        }

        affiliate_user_id = self.get_affiliate_user_id(user_id)
        if affiliate_user_id is None:
            raise ValueError("User is not registered.")

        # Update the affiliate_data offer identifier with the user's affiliate id.
        affiliate_data['id'] = affiliate_user_id
        return generate_tracking_link(affiliate_data, affiliate_user_id)