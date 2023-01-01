CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    allow_follow BOOLEAN DEFAULT true
);

CREATE TABLE moves (
    id SERIAL PRIMARY KEY,
    move_name TEXT UNIQUE,
    added_by INTEGER REFERENCES users
);

CREATE TABLE trainingtemplates (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    template_name TEXT
);

CREATE TABLE moves_in_template (
    template_id INTEGER REFERENCES trainingtemplates ON DELETE CASCADE,
    move_id INTEGER REFERENCES moves ON DELETE CASCADE
);