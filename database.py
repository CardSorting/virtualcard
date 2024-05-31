import sqlite3
import pandas as pd

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('cards.db')
        self.c = self.conn.cursor()
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS cards (
                id INTEGER PRIMARY KEY,
                Card_Name TEXT,
                "Set" TEXT,
                Type TEXT,
                Level INTEGER,
                Attribute TEXT,
                Rarity TEXT,
                Condition TEXT,
                Card_Effect TEXT,
                ATK INTEGER,
                DEF INTEGER,
                Spell_Category TEXT,
                Trap_Category TEXT,
                Price REAL,
                Inventory_Count INTEGER
            )
        ''')
        self.conn.commit()

    def load_data_to_db(self, data: pd.DataFrame):
        """Load data into the SQLite database."""
        data.to_sql('cards', self.conn, if_exists='replace', index=False)

    def retrieve_data_from_db(self) -> pd.DataFrame:
        """Retrieve data from the SQLite database."""
        return pd.read_sql('SELECT * FROM cards', self.conn)

    def export_to_excel(self, data: pd.DataFrame) -> str:
        """Export data to an Excel file."""
        file_path = "exported_collection.xlsx"
        data.to_excel(file_path, index=False)
        return file_path

    def fetch_data_from_db(self) -> pd.DataFrame:
        """Fetch data from the database."""
        return self.retrieve_data_from_db()