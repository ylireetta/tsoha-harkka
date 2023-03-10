from db import DB

def get_users_templates(user_id):
    sql = "SELECT T.id, T.template_name, \
        M.move_name, M.id AS move_id, M.visible, \
        MIT.number_of_sets \
        FROM trainingtemplates T, moves_in_template MIT, moves M \
        WHERE T.user_id=:user_id AND MIT.template_id=T.id AND M.id=MIT.move_id"
    result = DB.session.execute(sql, {"user_id":user_id})
    templates = result.fetchall()
    return templates

def create_template(user_id, template_name):
    sql = "INSERT INTO trainingtemplates (user_id, template_name) \
        VALUES (:user_id, :template_name) RETURNING id"
    result = DB.session.execute(sql, {"user_id":user_id, "template_name":template_name})
    DB.session.commit()
    return result.fetchone()["id"]

def add_to_reference_table(template_id, move_id, number_of_sets):
    sql = "INSERT INTO moves_in_template (template_id, move_id, number_of_sets) \
        VALUES (:template_id, :move_id, :number_of_sets)"
    DB.session.execute(
        sql,
        {"template_id":template_id,
        "move_id":move_id,
        "number_of_sets":number_of_sets}
    )
    DB.session.commit()

def delete_template(template_id):
    sql = "DELETE FROM trainingtemplates WHERE id=:template_id"
    DB.session.execute(sql, {"template_id":template_id})
    DB.session.commit()

def get_template_owner(template_id):
    sql = "SELECT user_id FROM trainingtemplates WHERE id=:template_id"
    result = DB.session.execute(sql, {"template_id":template_id})
    return result.fetchone()["user_id"]
