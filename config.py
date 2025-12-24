import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", 812242774))
CHANNEL_ID = int(os.getenv("CHANNEL_ID", -1003533914629))
DATA_DIR = os.getenv("DATA_DIR", "/app/data")

os.environ["DATA_DIR"] = DATA_DIR

if not BOT_TOKEN:
    print("WARNING: BOT_TOKEN is not set in .env file.")
