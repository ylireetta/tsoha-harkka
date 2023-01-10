from db import DB

def like(target_id, user_id):
    try:
        sql = "INSERT INTO actions (user_id, target_id, actiontype) VALUES (:user_id, :target_id, 'like')"
        DB.session.execute(sql, {"target_id":target_id, "user_id":user_id})
        DB.session.commit()
        return True
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
    sql = "SELECT user_id, target_id FROM actions WHERE actiontype='like' AND user_id=:user_id"
    result = DB.session.execute(sql, {"user_id":user_id})
    return result.fetchall()