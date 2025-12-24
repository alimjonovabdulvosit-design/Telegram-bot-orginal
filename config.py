import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))
CHANNEL_ID = int(os.getenv("CHANNEL_ID", 0))
DATA_DIR = os.getenv("DATA_DIR", "/app/data")

# Export to environment for other modules
os.environ["DATA_DIR"] = DATA_DIR

if not BOT_TOKEN:
    print("CRITICAL: BOT_TOKEN environment variable is missing!")
