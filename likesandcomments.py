from db import DB

def like(target_id, user_id):
    try:
        sql = "INSERT INTO actions (user_id, target_id, actiontype, actiondate) \
            VALUES (:user_id, :target_id, 'like', NOW()) RETURNING id"
        result = DB.session.execute(sql, {"target_id":target_id, "user_id":user_id})
        DB.session.commit()
        return result.fetchone()["id"]
    except:
        return False

def remove_like(target_id, user_id):
    try:
        sql = "DELETE FROM actions WHERE target_id=:target_id AND user_id=:user_id"
        DB.session.execute(sql, {"target_id":target_id, "user_id":user_id})
        DB.session.commit()
        return True
    except:
        return False

def get_likes_by_user(user_id):
    sql = "SELECT user_id, target_id FROM actions \
        WHERE actiontype='like' AND user_id=:user_id"
    result = DB.session.execute(sql, {"user_id":user_id})
    return result.fetchall()

def add_comment(user_id, target_id, content):
    try:
        sql = "INSERT INTO actions (user_id, target_id, actiontype, content, actiondate) \
            VALUES (:user_id, :target_id, 'comment', :content, NOW()) RETURNING id"
        result = DB.session.execute(
            sql,
            {"user_id":user_id,
            "target_id":target_id,
            "content":content}
        )
        DB.session.commit()
        return result.fetchone()["id"]
    except:
        return False

def remove_comment(comment_id, user_id):
    try:
        # Double-triple-checking that everything is ok: query w/ user id and action type as well.
        sql = "DELETE FROM actions \
            WHERE id=:comment_id AND user_id=:user_id AND actiontype='comment'"
        DB.session.execute(sql, {"comment_id":comment_id, "user_id":user_id})
        DB.session.commit()
        return True
    except:
        return False

def get_comments(target_id):
    sql = "SELECT A.id, A.user_id, U.username, A.content, A.actiondate \
        FROM actions A, users U \
        WHERE A.target_id=:target_id AND U.id=A.user_id AND A.actiontype='comment'"
    result = DB.session.execute(sql, {"target_id":target_id})
    return result.fetchall()

def get_action_owner(action_id):
    sql = "SELECT user_id FROM actions WHERE id=:action_id"
    result = DB.session.execute(sql, {"action_id":action_id})
    return result.fetchone()["user_id"]

def get_related_session(action_id):
    sql = "SELECT target_id FROM actions WHERE id=:action_id"
    result = DB.session.execute(sql, {"action_id":action_id})
    return result.fetchone()["target_id"]
