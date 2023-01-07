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
    recent_sessions = result.fetchall()
    return recent_sessions

def get_session_data(user_id, session_id):
    sql = "SELECT M.id AS move_id, M.move_name, S.reps, S.weights, TS.created_at \
        FROM sets S \
        LEFT JOIN trainingsessions TS ON TS.id=S.session_id \
        LEFT JOIN moves M ON S.move_id=M.id \
        WHERE TS.completed=true AND TS.user_id=:user_id AND TS.id=:session_id \
        ORDER BY M.id"
    result = DB.session.execute(sql, {"user_id":user_id, "session_id":session_id})
    session_data = result.fetchall()
    return session_data

def get_recent_max_weights(user_id):
    sql = "SELECT DISTINCT \
        ON (M.id) M.id, S.session_id, M.move_name, S.reps, S.weights, TS.created_at \
        FROM sets S JOIN trainingsessions TS ON session_id=TS.id \
        JOIN moves M on move_id=M.id \
        WHERE TS.completed=true AND TS.user_id=:user_id \
        ORDER BY M.id, S.weights DESC, TS.created_at DESC"

    result = DB.session.execute(sql, {"user_id":user_id})
    rows = result.fetchall()
    return rows