CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    allow_follow BOOLEAN DEFAULT true
);

CREATE TABLE moves (
    id SERIAL PRIMARY KEY,
    move_name TEXT UNIQUE,
    added_by INTEGER REFERENCES users,
    visible BOOLEAN DEFAULT true
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

CREATE TABLE trainingsessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    created_at TIMESTAMP,
    completed BOOLEAN DEFAULT false
);

CREATE TABLE sets (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    session_id INTEGER REFERENCES trainingsessions,
    move_id INTEGER REFERENCES moves,
    reps INTEGER,
    weights REAL
);

CREATE TABLE followedusers (
    id SERIAL PRIMARY KEY,
    follower_id INTEGER REFERENCES users,
    followed_user_id INTEGER REFERENCES users
);

CREATE TABLE actions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    target_id INTEGER REFERENCES trainingsessions,
    actiontype TEXT,
    content TEXT
);