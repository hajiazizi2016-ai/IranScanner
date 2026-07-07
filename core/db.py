import sqlite3

class DB:

    def __init__(self):
        self.conn = sqlite3.connect("market.db")
        self.create_table()
        print("SQLite DB initialized")

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS signals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT,
            price REAL,
            volume REAL,
            score REAL
        )
        """)
        self.conn.commit()

    def save_signals(self, signals):
        cursor = self.conn.cursor()

        for s in signals:
            cursor.execute("""
            INSERT INTO signals (symbol, price, volume, score)
            VALUES (?, ?, ?, ?)
            """, (s["symbol"], s["price"], s["volume"], s["score"]))

        self.conn.commit()

    def fetch_all(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM signals ORDER BY score DESC")
        return cursor.fetchall()