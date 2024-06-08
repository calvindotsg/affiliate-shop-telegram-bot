from decouple import config

TELEGRAM_BOT_TOKEN: str = str(object=config('TELEGRAM_BOT_TOKEN', default=None))