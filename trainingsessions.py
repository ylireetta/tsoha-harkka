from db import DB

def add_training_session(user_id):
    try:
        sql = "INSERT INTO trainingsessions (user_id, created_at) VALUES (:user_id, NOW()) RETURNING id"
        result = DB.session.execute(sql, {"user_id":user_id})
        DB.session.commit()
        return result.fetchone()["id"]
    except:
        return False

def add_set(user_id, session_id, move_id, reps, weights):
    try:
        # Looping through all received sets. Add them to db.
        # Change training session to completed if all goes well.
        sql = "INSERT INTO sets (user_id, session_id, move_id, reps, weights) VALUES (:user_id, :session_id, :move_id, :reps, :weights)"
        DB.session.execute(sql, {"user_id":user_id, "session_id":session_id, "move_id":move_id, "reps":reps, "weights":weights})
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