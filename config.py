import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "8529469877:AAHb5ct0exDCeZzOsRUtshXScjvyH4LI3EE")
ADMIN_ID = int(os.getenv("ADMIN_ID", 812242774))
CHANNEL_ID = int(os.getenv("CHANNEL_ID", -1003533914629))
DATA_DIR = os.getenv("DATA_DIR", "/app/data")

# Export to environment for other modules
os.environ["DATA_DIR"] = DATA_DIR

REQUIRED_CHANNEL_ID = int(os.getenv("REQUIRED_CHANNEL_ID", -1003581883170))
REQUIRED_CHANNEL_URL = "https://t.me/c/3581883170/1"

if not BOT_TOKEN:
    print("CRITICAL: BOT_TOKEN environment variable is missing!")
