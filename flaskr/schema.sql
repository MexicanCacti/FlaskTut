DROP TABLE IF EXISTS user; /*Delete 'user' table if exists, otherwise do nothing */
DROP TABLE IF EXISTS post;

CREATE TABLE user(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE post(
    id INTEGER PRIMARY KEY AUTOINCREMENT, /*Column name, data type, primiary key (Unique & not null), id auto increase w/ records */
    author_id INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, /*Column name, store data & time values, can't have NULL, sets default value to current data&time */
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    FOREIGN KEY (author_id) REFERENCES user (id) /* Declares author_id column a foreign key, Author_id must correspond to id column in user table */
);

