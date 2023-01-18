from db import DB

def create_notification(action_id):
    sql = "INSERT INTO notifications (action_id) VALUES (:action_id)"
    DB.session.execute(sql, {"action_id":action_id})
    DB.session.commit()

def mark_as_seen(notification_id):
    sql = "UPDATE notifications SET (seen, seen_at)=(true, NOW()) WHERE id=:notification_id"
    DB.session.execute(sql, {"notification_id":notification_id})
    DB.session.commit()

def get_users_notifications(user_id):
    sql = "SELECT N.id, A.user_id, U.username, A.target_id, A.actiontype, A.actiondate, A.content \
        FROM actions A, notifications N, users U, trainingsessions TS \
        WHERE N.seen=false AND N.action_id=A.id AND U.id=A.user_id AND TS.id=A.target_id AND TS.user_id=:user_id"
    result = DB.session.execute(sql, {"user_id":user_id})
    return result.fetchall()

def get_notiftarget_owner(notification_id):
    sql = "SELECT TS.user_id FROM actions A, notifications N, trainingsessions TS \
        WHERE A.id=N.action_id AND A.target_id=TS.id AND N.id=:notification_id"
    result = DB.session.execute(sql, {"notification_id":notification_id})
    return result.fetchone()["user_id"]
