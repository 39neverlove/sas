import sqlite3
from contextlib import contextmanager

class Database:
    def __init__(self, db_name="steam_bot.db"):
        self.db_name = db_name
        self.init_db()

    def init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # Таблица пользователей
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    telegram_id INTEGER PRIMARY KEY,
                    username TEXT,
                    language TEXT DEFAULT 'ru',
                    referrals INTEGER DEFAULT 0,
                    created_accounts INTEGER DEFAULT 0,
                    is_blocked INTEGER DEFAULT 0
                )
            """)
            # Таблица аккаунтов
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS accounts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    login TEXT,
                    password TEXT,
                    email TEXT,
                    region TEXT,
                    user_id INTEGER,
                    FOREIGN KEY (user_id) REFERENCES users (telegram_id)
                )
            """)
            # Таблица рефералов
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS referrals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    referrer_id INTEGER,
                    referred_id INTEGER,
                    FOREIGN KEY (referrer_id) REFERENCES users (telegram_id),
                    FOREIGN KEY (referred_id) REFERENCES users (telegram_id)
                )
            """)
            conn.commit()

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_name)
        try:
            yield conn
        finally:
            conn.close()