from flask import render_template, request, redirect, session, flash
from app import APP
import users
import moves
import templates
import trainingsessions
import likesandcomments

@APP.route("/")
def index():
    followed_sessions = None
    liked_by_user = None
    if session.get("user_id"):
        followed_sessions = trainingsessions.get_followed_sessions(session["user_id"])
        liked_by_user = likesandcomments.get_likes_by_user(session["user_id"])

    return render_template(
        "index.html", 
        followed_sessions=followed_sessions, 
        liked_by_user=liked_by_user
    )

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

    return redirect("/")

@APP.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("user_id", None)
    return redirect("/")

@APP.route("/moveslibrary")
def moveslibrary():
    if not session.get("user_id"):
        return redirect("/")

    render_moves = None

    if "query" in request.args:
        query = request.args["query"]
        if "showmineonly" in request.args:
            render_moves = moves.search_moves(query, user_id=session["user_id"])
        else:
            render_moves = moves.search_moves(query)
    else:
        render_moves = moves.get_moves()

    return render_template("moveslibrary.html", moves=render_moves)

@APP.route("/profile", methods=["GET", "POST"])
def profile():
    if not session.get("user_id"):
        return redirect("/")

    render_moves = moves.get_moves()
    my_templates = templates.get_users_templates(session["user_id"])

    # This is ugly.
    complete_templates = []
    if len(my_templates) > 0:
        template_moves = []
        last_id = my_templates[0]["id"]
        last_name = my_templates[0]["template_name"]
        index = 0

        for row in my_templates:
            index = index + 1
            # Case 1: We are still looking at a row that belongs to a template we have already seen.
            # Append move to array and keep going.
            if last_id == row["id"]:
                template_moves.append(row["move_name"])
            # Case 2: No longer the same template.
            # Append the data we collected earlier to the final boss array.
            # Set variables so that we can keep going.
            if row["id"] != last_id:
                moves_string = ", ".join(template_moves)
                complete_templates.append((last_name, moves_string, row["id"]))
                last_id = row["id"]
                last_name = row["template_name"]
                template_moves = []
                # Append the first move of new template row,
                # since we just "cleared" the whole move array.
                # Note that clear() does not actually work for some reason.
                template_moves.append(row["move_name"])
            # Case 3: We reached the last row of the table.
            # It has the same id as the former one, so check index against length of result table.
            if index == len(my_templates):
                moves_string = ", ".join(template_moves)
                complete_templates.append((row["template_name"], moves_string, row["id"]))

    # Get current value from database.
    allow_follow_value = bool(users.get_allow_follow(session["username"])[0])

    if request.method == "POST" and "allow_follow" in request.form:
        success = users.update_user(session["username"], request.form["allow_follow"])

        if not success:
            flash("Could not update allow_follow.", "alert alert-danger")
        else:
            flash("Allow_follow successfully updated!", "alert alert-success")
            allow_follow_value = request.form["allow_follow"].lower() == "true"

    return render_template(
        "profile.html",
        allow_follow_value=allow_follow_value,
        moves=render_moves,
        users_templates=my_templates,
        complete_templates=complete_templates
    )

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

    all_moves = moves.get_moves()
    moves_result = []

    for row in all_moves:
        moves_result.append(dict(row))

    users_templates = templates.get_users_templates(session["user_id"])
    all_templates = []

    for row in users_templates:
        all_templates.append(dict(row))

    users_sessions = trainingsessions.get_recent_sessions(session["user_id"])
    sessions = []

    for row in users_sessions:
        sessions.append(dict(row))

    recent_max = trainingsessions.get_recent_max_weights(session["user_id"])
    max_weights = []

    for row in recent_max:
        max_weights.append(dict(row))

    return render_template(
        "trainingdata.html",
        data_view_moves=moves_result,
        templates=all_templates,
        sessions=sessions,
        max_weights=max_weights
    )

@APP.route("/addtrainingsession", methods=["GET", "POST"])
def add_training_session():
    # https://stackoverflow.com/questions/50146815/getting-multiple-html-fields-with-same-name-using-getlist-with-flask-in-python
    if request.method == "POST":
        user_id = session["user_id"]
        session_id = trainingsessions.add_training_session(user_id)

        if isinstance(session_id, int):
            submitted_move_list = request.form.getlist("selected_moves")
            submitted_reps_list = request.form.getlist("reps")
            submitted_weights_list = request.form.getlist("weights")

            for move, reps, weights in zip(submitted_move_list,
            submitted_reps_list, submitted_weights_list):
                if not trainingsessions.add_set(user_id, session_id, move, reps, weights):
                    flash(
                        f"Could not add set for move id {move}, aborting database operation.",
                        "alert alert-danger"
                    )
                    break
            if trainingsessions.complete_session(session_id):
                flash("Training session successfully saved!", "alert alert-success")
        else:
            flash("Could not create new training session.", "alert alert-danger")

    return redirect("/trainingdata")

@APP.route("/createtemplate", methods=["GET", "POST"])
def create_template():
    # If a user types in url directly, redirect.
    if request.method == "GET":
        return redirect("/profile")

    if len(request.form.getlist("selected_moves")) == 0:
        flash("Please select moves when creating a training template.", "alert alert-danger")
        return redirect("/profile")

    creation_ret = templates.create_template(session["user_id"], request.form["template_name"])
    if isinstance(creation_ret, int):
        # Get selected move ids as list.
        selected_moves = request.form.getlist("selected_moves")
        for move_id in selected_moves:
            templates.add_to_reference_table(creation_ret, int(move_id))
        flash("Template saved successfully!", "alert alert-success")
    else:
        flash("Could not create new template.", "alert alert-danger")

    return redirect("/profile")

@APP.route("/deletetemplate/<int:id_>", methods=["GET", "POST"])
def delete_template(id_):
    if templates.delete_template(id_):
        flash(f"Template {id_} deleted!", "alert alert-success")
    else:
        flash(f"Could not delete template {id_}.", "alert alert-danger")
    return redirect("/profile")

@APP.route("/deletemove/<int:id_>", methods=["GET", "POST"])
def delete_move(id_):
    if moves.delete_move(id_):
        flash(f"Move {id_} deleted!", "alert alert-success")
    else:
        flash(f"Could not delete move {id_}.", "alert alert-danger")
    return redirect("/moveslibrary")

@APP.route("/trainingsession/<int:id_>", methods=["GET"])
def get_trainingsessions(id_):
    session_data = trainingsessions.get_session_data(session["user_id"], id_)

    if session_data:
        session_comments = likesandcomments.get_comments(id_)
        main_info = {
            "session_id": id_,
            "username": session_data[0].username,
            "created_at": session_data[0].created_at
        }
        return render_template("trainingsession.html", sessions=session_data, comments=session_comments, main_info=main_info)
    else:
        flash(f"No session with id {id_} found.", "alert alert-danger")
        return redirect("/")

@APP.route("/userdata", methods=["GET"])
def userdata():
    userlist = users.get_userlist_with_followinfo(session["user_id"])

    return render_template("userdata.html", users=userlist)

@APP.route("/followunfollow/<int:id_>", methods=["GET", "POST"])
def follow_unfollow(id_):
    if request.method == "POST":
        follow = "follow" in request.form

        if users.follow_unfollow(session["user_id"], id_, follow):
            flash(f"Follow information successfully updated for user {id_}.", "alert alert-success")
        else:
            flash(f"Failed to update follow information for user {id_}.", "alert alert-danger")

    return redirect("/userdata")

@APP.route("/like/<int:id_>", methods=["POST"])
def toggle_like(id_):
    like = "like" in request.form

    if like:
        likesandcomments.like(id_, session["user_id"])
    else:
        likesandcomments.remove_like(id_, session["user_id"])
    
    return redirect("/")

@APP.route("/addcomment/<int:id_>", methods=["POST"])
def add_comment(id_):
    if request.method == "POST":
        content = request.form["commenttext"]

        if likesandcomments.add_comment(session["user_id"], id_, content):
            flash("Comment added!", "alert alert-success")
        else:
            flash("Could not add new comment.", "alert alert-danger")

    return redirect(f"/trainingsession/{id_}")

@APP.route("/removecomment/<int:id_>", methods=["POST"])
def remove_comment(id_):
    if likesandcomments.remove_comment(id_, session["user_id"]):
        flash("You deleted your comment successfully!", "alert alert-success")
    else:
        flash("Something went wrong - couldn't delete comment.", "alert alert-danger")

    return redirect(request.referrer)