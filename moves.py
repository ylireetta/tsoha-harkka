from db import db

def get_moves():
    sql = "SELECT id, name FROM moves"
    result = db.session.execute(sql)
    moves = result.fetchall()
    return moves

def search_moves(query):
    sql = "SELECT id, name FROM moves WHERE name LIKE :query"
    result = db.session.execute(sql, {"query": "%" + query + "%"})
    moves = result.fetchall()
    return moves

def add_move(new_move, user_id):
    
    try:
        sql = "INSERT INTO moves (name, added_by) VALUES (:name, :user_id)"
        db.session.execute(sql, {"name": new_move, "user_id": user_id})
        db.session.commit()
        return True
    except:
        return False