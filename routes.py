from flask import render_template, request, redirect, session, flash
from app import APP
import users
import moves
import templates

@APP.route("/")
def index():
    return render_template("index.html")

@APP.route("/register", methods=["GET", "POST"])
def register():
    # Method can be either GET or POST
    # GET: user requests the registration page to create a new account
    # POST: user has filled out the registration form and has clicked the submit button
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        if password1 != password2:
            flash("Password fields do not match.", "alert alert-danger")
            return redirect("/register")

        if not users.register_user(username, password1):
            flash("Registration unsuccessful.", "alert alert-danger")
            return redirect("/register")

    flash("Registered successfully - logged you in for convenience!", "alert alert-success")
    return redirect("/")


@APP.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not users.login(username, password):
            flash("Login unsuccessful - check username and password.", "alert alert-danger")

    return render_template("index.html")

@APP.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("user_id", None)
    return redirect("/")

@APP.route("/moveslibrary")
def moveslibrary():
    if not session.get("user_id"):
        return redirect("/")

    render_moves = ""

    if "query" in request.args:
        query = request.args["query"]
        render_moves = moves.search_moves(query)
    else:
        render_moves = moves.get_moves()

    return render_template("moveslibrary.html", moves=render_moves)

@APP.route("/profile", methods=["GET", "POST"])
def profile():
    if not session.get("user_id"):
        return redirect("/")

    # Get current value from database.
    allow_follow_value = bool(users.get_allow_follow(session["username"])[0])

    if request.method == "POST" and "allow_follow" in request.form:
        success = users.update_user(session["username"], request.form["allow_follow"])

        if not success:
            flash("Could not update allow_follow.", "alert alert-danger")
        else:
            flash("Allow_follow successfully updated!", "alert alert-success")
            allow_follow_value = request.form["allow_follow"].lower() == "true"

    return render_template("profile.html", allow_follow_value=allow_follow_value)

@APP.route("/addmove", methods=["GET", "POST"])
def add_move():
    # If a user types in url directly, redirect.
    if request.method == "GET":
        return redirect("/moveslibrary")

    move_name = request.form["movename"]
    user_id = session["user_id"]

    if not moves.add_move(move_name, user_id):
        flash(f"Could not add new move {move_name}.", "alert alert-danger")
        return redirect("/moveslibrary")

    flash(f"New move {move_name} successfully added!", "alert alert-success")
    return redirect("/moveslibrary")

@APP.route("/trainingdata", methods=["GET", "POST"])
def trainingdata():
    if not session.get("user_id"):
        return redirect("/")

    render_moves = moves.get_moves()
    my_templates = templates.get_users_templates(session["user_id"])

    # This is ugly.
    complete_templates = []
    if len(my_templates) > 0:
        template_moves = []
        last_ID = my_templates[0]["id"]
        last_name = my_templates[0]["template_name"]
        index = 0

        for row in my_templates:
            index = index + 1
            # Case 1: We are still looking at a row that belongs to a template we have already seen. Append move to array and keep going.
            if last_ID == row["id"]:
                template_moves.append(row["move_name"])
            # Case 2: No longer the same template. Append the data we collected earlier to the final boss array. Set variables so that we can keep going.
            if row["id"] != last_ID:
                moves_string = ", ".join(template_moves)
                complete_templates.append((last_name, moves_string))
                last_ID = row["id"]
                last_name = row["template_name"]
                template_moves = []
                template_moves.append(row["move_name"]) # Append the first move of new template row, since we just "cleared" the whole move array. Note that clear() does not actually work for some reason.
            # Case 3: We reached the last row of the table. It has the same id as the former one, so check index against length of result table.
            if index == len(my_templates):
                moves_string = ", ".join(template_moves)
                complete_templates.append((row["template_name"], moves_string))

    return render_template("trainingdata.html", moves=render_moves, users_templates=my_templates, complete_templates=complete_templates)

@APP.route("/createtemplate", methods=["GET", "POST"])
def create_template():
    # If a user types in url directly, redirect.
    if request.method == "GET":
        return redirect("/trainingdata")

    creation_ret = templates.create_template(session["user_id"], request.form["template_name"]) 
    if isinstance(creation_ret, int):       
        # Get selected move ids as list.
        selected_moves = request.form.getlist("selected_moves")
        for move_id in selected_moves:
            templates.add_to_reference_table(creation_ret, int(move_id))
        flash("Template saved successfully!", "alert alert-success")
    else:
        flash("Could not create new template.", "alert alert-danger")

    return redirect("/trainingdata")