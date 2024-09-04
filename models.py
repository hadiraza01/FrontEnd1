import sqlite3

class UserDatabase:
    def __init__(self, db_path='database.db'):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS doctors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )
            ''')
            conn.commit()

    def query_db(self, query, args=(), one=False):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, args)
            rv = cursor.fetchall()
            conn.commit()
        return (rv[0] if rv else None) if one else rv

    def insert_user(self, username, password):
        self.query_db('INSERT INTO doctors (username, password) VALUES (?, ?)', (username, password))

    def get_user(self, username, password=None):
        if password:
            return self.query_db('SELECT * FROM doctors WHERE username = ? AND password = ?', (username, password), one=True)
        return self.query_db('SELECT * FROM doctors WHERE username = ?', (username,), one=True)