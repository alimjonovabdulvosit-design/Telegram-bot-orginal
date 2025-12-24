import aiosqlite
import os
import logging

logger = logging.getLogger(__name__)

DB_DIR = os.getenv("DATA_DIR", ".")
DB_NAME = os.path.join(DB_DIR, "bot_database.db")

async def init_db():
    # Ensure directory exists
    if DB_DIR != "." and not os.path.exists(DB_DIR):
        try:
            os.makedirs(DB_DIR, exist_ok=True)
            logger.info(f"Created directory: {DB_DIR}")
        except Exception as e:
            logger.error(f"Could not create directory {DB_DIR}: {e}")
            # Fallback to current directory if specified DATA_DIR fails
            global DB_NAME
            DB_NAME = "bot_database.db"
            logger.warning("Falling back to current directory for database.")

    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                status TEXT DEFAULT 'free',
                username TEXT
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                amount INTEGER,
                status TEXT DEFAULT 'pending',
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()

async def add_user(user_id, username):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
        await db.commit()

async def get_user_status(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT status FROM users WHERE user_id = ?", (user_id,)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else None

async def update_user_status(user_id, status):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("UPDATE users SET status = ? WHERE user_id = ?", (status, user_id))
        await db.commit()

async def create_payment_request(user_id, amount):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("INSERT INTO payments (user_id, amount) VALUES (?, ?)", (user_id, amount))
        await db.commit()
