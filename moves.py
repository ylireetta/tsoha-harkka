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

def add_move(new_move):
    
    try:
        sql = "INSERT INTO moves (name) VALUES (:name)"
        db.session.execute(sql, {"name": new_move})
        db.session.commit()
        return True
    except:
        return False