from db import DB

def get_moves():
    sql = "SELECT id, move_name FROM moves WHERE visible=true"
    result = DB.session.execute(sql)
    moves = result.fetchall()
    return moves

def search_moves(query, **kwargs):
    user_id = kwargs.get("user_id", None)

    if user_id:
        sql = "SELECT id, move_name FROM moves \
            WHERE move_name LIKE :query AND added_by=:user_id AND visible=true"
        result = DB.session.execute(sql, {"query": "%" + query + "%", "user_id":user_id})
    else:
        sql = "SELECT id, move_name FROM moves WHERE move_name LIKE :query AND visible=true"
        result = DB.session.execute(sql, {"query": "%" + query + "%"})
    moves = result.fetchall()
    return moves

def add_move(new_move, user_id):
    try:
        sql = "INSERT INTO moves (move_name, added_by) VALUES (:name, :user_id)"
        DB.session.execute(sql, {"name": new_move, "user_id": user_id})
        DB.session.commit()
        return True
    except:
        return False

def delete_move(move_id):
    try:
        sql = "UPDATE moves SET visible=false WHERE id=:move_id"
        DB.session.execute(sql, {"move_id":move_id})
        DB.session.commit()
        return True
    except:
        return False
