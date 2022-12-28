from db import db

def get_moves():
    sql = "SELECT * FROM moves"
    result = db.session.execute(sql)
    moves = result.fetchall()
    return moves

def search_moves(query):
    sql = "SELECT id, name FROM moves WHERE name LIKE :query"
    result = db.session.execute(sql, {"query": "%" + query + "%"})
    moves = result.fetchall()
    return moves