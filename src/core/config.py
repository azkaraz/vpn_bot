import os
from dotenv import load_dotenv

load_dotenv()

MONGO_DB_URL = os.getenv('MONGO_DB_URL')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
MONGO_URL = os.getenv('MONGO_URL')
MONGO_DB = os.getenv('MONGO_DB')
WALLET_TOKEN = os.getenv('WALLET_TOKEN')
SUBSCRIPTION_PRICE = os.getenv('SUBSCRIPTION_PRICE')
WIREGUARD_URL = os.getenv('WIREGUARD_URL')
WIREGUARD_PASSWORD = os.getenv('WIREGUARD_PASSWORD')