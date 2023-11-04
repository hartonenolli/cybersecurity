CREATE TABLE person (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE info_message (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES person,
    time TIMESTAMP,
    memo TEXT
);

CREATE TABLE info_comment (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES person,
    notes_id INTEGER REFERENCES info_message,
    time TIMESTAMP,
    comment TEXT
);

BEGIN TRANSACTION;
INSERT INTO person (username, password) VALUES ('arska', 'arska123');
INSERT INTO person (username, password) VALUES ('user', 'user123');
COMMIT;
