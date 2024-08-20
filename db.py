import sqlite3

class DB:
    def __init__(self):
        self.conn=None
        self.cursor=None

    def connect(self):
        self.conn = sqlite3.connect('rss.db', check_same_thread=False)
        self.cursor = self.conn.cursor()

    def prepare(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS subscriptions (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                url TEXT NOT NULL,
                unique(user_id, url)
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users(
                id UNTEGER UNIQUE
            )
        ''')
        self.conn.commit()
    
    def add_user(self, user_id):
        self.cursor.execute("INSERT INTO users(id) VALUES(?)", (user_id))
        self.conn.commit()

    def add_subscription(self, user_id, url):
        self.cursor.execute("INSERT INTO subscriptions(user_id, url) VALUES(?,?)", (user_id, url))
        self.conn.commit()

    def get_users_subscriptions(self):
        self.cursor.execute('SELECT user_id, url FROM subscriptions')
        return self.cursor.fetchall()