from werkzeug.security import check_password_hash, generate_password_hash
from flask import session
from db import DB

def register_user(username, password):
    hash_pass = generate_password_hash(password)

    # Users need to have unique usernames, so use try-except.
    try:
        sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
        DB.session.execute(sql, {"username":username, "password":hash_pass})
        DB.session.commit()
    except:
        return False
    return login(username, password)

def login(username, password):
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = DB.session.execute(sql, {"username": username})
    user = result.fetchone()

    if user and check_password_hash(user.password, password):
        session["username"] = username
        session["user_id"] = user.id
        return True

    return False

def update_user(username, allow_follow):
    sql = "UPDATE users SET allow_follow=:allow_follow WHERE username=:username"
    bool_value = allow_follow.lower() == "true"
    DB.session.execute(sql, {"username": username, "allow_follow": bool_value})
    DB.session.commit()

def get_allow_follow(username):
    sql = "SELECT allow_follow FROM users WHERE username=:username"
    result = DB.session.execute(sql, {"username": username})
    return result.fetchone()["allow_follow"]

def follow_unfollow(follower_id, followed_user_id, follow):
    if follow:
        sql = "INSERT INTO followedusers (follower_id, followed_user_id) \
            VALUES (:follower_id, :followed_user_id)"
    else:
        sql = "DELETE FROM followedusers \
            WHERE follower_id=:follower_id AND followed_user_id=:followed_user_id"

    DB.session.execute(sql, {"follower_id":follower_id, "followed_user_id":followed_user_id})
    DB.session.commit()

def get_userlist_with_followinfo(user_id):
    sql = "SELECT U.id, U.username, U.allow_follow, F.followed_user_id, F.follower_id \
        FROM users U\
        LEFT JOIN \
            (SELECT follower_id, followed_user_id \
            FROM followedusers \
            WHERE follower_id=:user_id) AS F \
        ON F.followed_user_id=U.id"
    result = DB.session.execute(sql, {"user_id":user_id})
    return result.fetchall()
