from werkzeug.security import check_password_hash, generate_password_hash
from db import db
from flask import session

def get_users():
    sql = "SELECT * FROM users"
    result = db.session.execute(sql)
    users = result.fetchall()
    return users

def register_user(username, password):
    hash_pass = generate_password_hash(password)

    try:
        sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
        db.session.execute(sql, {"username":username, "password":hash_pass})
        db.session.commit()
    except:
        return False
    return True

def login(username, password):
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()

    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["username"] = username
            session["user_id"] = user.id
            return True
        else:
            return False

def update_user(username, allow_follow):
    sql = "UPDATE users SET allow_follow=:allow_follow WHERE username=:username"
    bool_value = allow_follow.lower() == "true"

    try:
        db.session.execute(sql, {"username": username, "allow_follow": bool_value})
        db.session.commit()
        return True
    except:
        return False

def get_allow_follow(username):
    sql = "SELECT allow_follow FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    return result.fetchone()