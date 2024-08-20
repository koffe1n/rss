CREATE TABLE IF NOT EXISTS subscriptions (
    user_id INTEGER NOT NULL,
    rss_id INTEGER NOT NULL,
    CONSTRAINT fk_user FOREIGN KEY(user_id) REFERENCES users(user_id)
    CONSTRAINT fk_rss FOREIGN KEY(rss_id) REFERENCES rss(id)
);

CREATE TABLE IF NOT EXISTS rss(
    id INTEGER PRIMARY KEY,
    url VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER NOT NULL PRIMARY KEY,
    username VARCHAR(255) NOT NULL
);