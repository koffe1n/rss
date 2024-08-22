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
            );''')
        self.cursor.execute('''               
             CREATE TABLE IF NOT EXISTS rss(
                id INTEGER PRIMARY KEY,
                url VARCHAR(255) UNIQUE NOT NULL
            );'''
        )
        self.cursor.execute('''                    
            CREATE TABLE IF NOT EXISTS users_sources(
                id INTEGER PRIMARY KEY,
                name VARCHAR(15) NOT NULL
            );''')
        self.cursor.execute('''                    
            INSERT INTO users_sources(name) 
            VALUES("telegram"),("discord");''')
        self.cursor.execute('''                    
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER NOT NULL PRIMARY KEY,
                username VARCHAR(255) NOT NULL,
                source_id INTEGER NOT NULL,
                CONSTRAINT fk_source FOREIGN KEY(source_id) REFERENCES users_sources(id)
            );'''
        )
        self.conn.commit()
    
    def add_user(self, user_id, username, source):
        self.cursor.execute('''INSERT INTO users(id, username, source_id)
                             VALUES(?,?,(SELECT id FROM users_sources WHERE name=?))''', 
                             (user_id, username, source))
        self.conn.commit()

    def add_subscription(self, user_id, url):
        self.cursor.execute("INSERT INTO rss(url) VALUES(?) ON CONFLICT DO NOTHING", (url,))
        # TODO lastrowid works bad. fix on pg -> do update return id
        self.cursor.execute("SELECT id FROM rss WHERE url=?", (url,))
        rss_id = self.cursor.fetchone()[0]
        self.cursor.execute("INSERT INTO subscriptions(user_id, rss_id) VALUES(?,?)", (user_id, rss_id))
        self.conn.commit()

    def delete_subscription(self, user_id, url):
        self.cursor.execute('''DELETE FROM subscriptions WHERE rss_id=(
                            SELECT id FROM rss WHERE url=?
                            ) AND user_id=?''', (url,user_id))
        # TODO remove unsubsribed links
        self.conn.commit()

    def get_all_users_subscriptions(self, source):
        self.cursor.execute('''SELECT s.user_id, r.url FROM subscriptions s
                            INNER JOIN rss r ON s.rss_id=r.id
                            INNER JOIN users u ON s.user_id=u.id
                            INNER JOIN users_sources us ON us.id=u.source_id
                            WHERE us.name=?
                            ''', (source,))
        return self.cursor.fetchall()