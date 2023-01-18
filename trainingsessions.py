from db import DB

def add_training_session(user_id):
    try:
        sql = "INSERT INTO trainingsessions (user_id, created_at) \
            VALUES (:user_id, NOW()) RETURNING id"
        result = DB.session.execute(sql, {"user_id":user_id})
        DB.session.commit()
        return result.fetchone()["id"]
    except:
        return False

def add_set(user_id, session_id, move_id, reps, weights):
    try:
        # Looping through all received sets. Add them to db.
        # Change training session to completed if all goes well.
        sql = "INSERT INTO sets (user_id, session_id, move_id, reps, weights) \
            VALUES (:user_id, :session_id, :move_id, :reps, :weights)"
        DB.session.execute(sql, {
            "user_id":user_id,
            "session_id":session_id,
            "move_id":move_id,
            "reps":reps,
            "weights":weights
        })
        DB.session.commit()
        return True
    except:
        return False

def complete_session(session_id):
    try:
        sql = "UPDATE trainingsessions SET completed=true WHERE id=:session_id"
        DB.session.execute(sql, {"session_id":session_id})
        DB.session.commit()
        return True
    except:
        return False

def get_recent_sessions(user_id):
    # Get table with data of completed workout sessions.
    sql = "SELECT TS.id, TS.created_at, M.move_name, S.reps, S.weights \
        FROM sets S \
        JOIN trainingsessions TS ON session_id=TS.id \
        JOIN moves M ON move_id=M.id \
        WHERE TS.completed=true AND TS.user_id=:user_id"
    result = DB.session.execute(sql, {"user_id":user_id})
    return result.fetchall()

def get_session_data(user_id, session_id):
    sql = "SELECT U.username, M.id AS move_id, M.move_name, S.reps, S.weights, TS.created_at, \
        (SELECT COUNT(*) FROM actions WHERE target_id=:session_id AND actiontype='like') AS likes, \
        CASE WHEN :user_id IN \
            (SELECT user_id FROM actions WHERE target_id=:session_id) \
            THEN true ELSE false END AS liked_by_current_user  \
        FROM sets S \
        LEFT JOIN users U ON U.id=S.user_id \
        LEFT JOIN trainingsessions TS ON TS.id=S.session_id \
        LEFT JOIN moves M ON S.move_id=M.id \
        WHERE TS.completed=true AND TS.id=:session_id \
        AND U.allow_follow=true \
        ORDER BY M.id"
        # Add condition TS.user_id=:user_id
        # if we need to restrict who can see individual session pages
        # (only session owner is then able to view records).
    result = DB.session.execute(sql, {"user_id":user_id, "session_id":session_id})
    return result.fetchall()

def get_recent_max_weights(user_id):
    sql = "SELECT DISTINCT \
        ON (M.id) M.id, S.session_id, M.move_name, S.reps, S.weights, TS.created_at \
        FROM sets S JOIN trainingsessions TS ON session_id=TS.id \
        JOIN moves M on move_id=M.id \
        WHERE TS.completed=true AND TS.user_id=:user_id \
        ORDER BY M.id, S.weights DESC, TS.created_at DESC"
    result = DB.session.execute(sql, {"user_id":user_id})
    return result.fetchall()

def get_followed_sessions(user_id, **kwargs):
    max_date = kwargs.get("max_date", None)

    # Get training sessions added by users who current user follows.
    # Include also info about likes.
    sql = "SELECT \
            U.id AS user_id, U.username, \
            S.session_id AS ses_id, S.reps, S.weights, TS.created_at, \
            M.move_name, \
            CASE WHEN :user_id IN \
                (SELECT user_id FROM actions WHERE target_id=S.session_id) \
            THEN true ELSE false END AS liked_by_current_user, \
            (SELECT COUNT(*) FROM actions WHERE target_id=S.session_id AND actiontype='like') AS likes \
        FROM users U, sets S, trainingsessions TS, moves M \
        WHERE U.id=S.user_id AND TS.id=S.session_id AND M.id=S.move_id AND TS.completed=true \
        AND TS.user_id IN \
            (SELECT followed_user_id FROM followedusers WHERE follower_id=:user_id)"

    if max_date:
        sql = sql + " AND TS.created_at>=date :max_date"
    sql = sql + " ORDER BY TS.created_at DESC"
    if max_date:
        result = DB.session.execute(sql, {"user_id":user_id, "max_date":max_date})
    else:
        result = DB.session.execute(sql, {"user_id":user_id})
    return result.fetchall()

def get_session_owner(session_id):
    sql = "SELECT user_id FROM trainingsessions WHERE id=:session_id"
    result = DB.session.execute(sql, {"session_id":session_id})
    return result.fetchone()["user_id"]
