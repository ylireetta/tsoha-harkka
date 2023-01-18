from db import DB

def get_moves():
    sql = "SELECT id, move_name, added_by \
        FROM moves \
        WHERE visible=true"
    result = DB.session.execute(sql)
    moves = result.fetchall()
    return moves

def search_moves(query, **kwargs):
    user_id = kwargs.get("user_id", None)

    if user_id:
        sql = "SELECT id, move_name, added_by \
            FROM moves \
            WHERE move_name LIKE LOWER(:query) AND added_by=:user_id AND visible=true"
        result = DB.session.execute(sql, {"query": "%" + query + "%", "user_id":user_id})
    else:
        sql = "SELECT id, move_name, added_by \
            FROM moves \
            WHERE move_name LIKE LOWER(:query) AND visible=true"
        result = DB.session.execute(sql, {"query": "%" + query + "%"})
    moves = result.fetchall()
    return moves

def add_move(new_move, user_id):
    # All visible moves need to have a unique name, so use try-except.
    try:
        sql = "INSERT INTO moves (move_name, added_by) VALUES (LOWER(:name), :user_id)"
        DB.session.execute(sql, {"name": new_move, "user_id": user_id})
        DB.session.commit()
        return True
    except:
        return False

def delete_move(move_id):
    sql = "UPDATE moves SET visible=false \
        WHERE id=:move_id"
    DB.session.execute(sql, {"move_id":move_id})
    DB.session.commit()

def get_move_owner(move_id):
    sql = "SELECT added_by \
        FROM moves \
        WHERE id=:move_id"
    result = DB.session.execute(sql, {"move_id":move_id})
    return result.fetchone()["added_by"]
