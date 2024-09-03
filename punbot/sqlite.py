import sqlite3

from punbot.gme_api import Prices


class SQLite:
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def create_table(self) -> None:
        self.cursor.execute(
            """\
CREATE TABLE IF NOT EXISTS prices
(id INTEGER PRIMARY KEY, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP, pun REAL, mgp REAL)
            """,
        )
        self.conn.commit()

    def insert(self, prices: Prices) -> None:
        self.cursor.execute(
            "INSERT INTO prices (pun, mgp) VALUES (?, ?)",
            (prices.pun, prices.mgp),
        )
        self.conn.commit()

    def get_n_average(self, n: int) -> Prices:
        self.cursor.execute(
            "SELECT AVG(pun), AVG(mgp) FROM (SELECT * FROM prices ORDER BY timestamp DESC LIMIT ?)",
            (n,),
        )
        prices = self.cursor.fetchone()
        return Prices(pun=prices[0], mgp=prices[1])

    def __del__(self):
        self.conn.close()
