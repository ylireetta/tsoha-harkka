CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    allow_follow BOOLEAN
);

CREATE TABLE moves (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    added_by INTEGER REFERENCES users
);