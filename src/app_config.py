from decouple import config

TELEGRAM_BOT_TOKEN: str = str(object=config('TELEGRAM_BOT_TOKEN', default=None))
FIRESTORE_CREDENTIAL_PATH: str = str(object=config('FIRESTORE_CREDENTIAL_PATH', default=None))
FIRESTORE_PROJECT_ID: str = str(object=config('FIRESTORE_PROJECT_ID', default=None))