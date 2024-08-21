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
                user_id INTEGER NOT NULL,
                rss_id INTEGER NOT NULL,
                CONSTRAINT fk_user FOREIGN KEY(user_id) REFERENCES users(user_id)
                CONSTRAINT fk_rss FOREIGN KEY(rss_id) REFERENCES rss(id)
            );
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS rss(
                id INTEGER PRIMARY KEY,
                url VARCHAR(255) UNIQUE NOT NULL
            );
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users(
                user_id INTEGER NOT NULL PRIMARY KEY,
                username VARCHAR(255) NOT NULL
            );
        ''')
        self.conn.commit()
    
    def add_user(self, user_id, username):
        self.cursor.execute("INSERT INTO users(user_id, username) VALUES(?,?)", (user_id, username))
        self.conn.commit()

    def add_subscription(self, user_id, url):
        self.cursor.execute("INSERT INTO rss(url) VALUES(?) ON CONFLICT DO NOTHING", (url,))
        self.cursor.execute("INSERT INTO subscriptions(user_id, rss_id) VALUES(?,?)", (user_id, self.cursor.lastrowid))
        self.conn.commit()

    def delete_subscription(self, user_id, url):
        self.cursor.execute('''DELETE FROM subscriptions WHERE rss_id=(
                            SELECT id FROM rss WHERE url=?
                            ) AND user_id=?''', (url,user_id))
        # TODO remove unsubsribed links
        self.conn.commit()

    def get_all_users_subscriptions(self):
        self.cursor.execute('''SELECT s.user_id, r.url FROM subscriptions s
                            INNER JOIN rss r ON s.rss_id=r.id
                            ''')
        return self.cursor.fetchall()