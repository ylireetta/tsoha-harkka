from flask import render_template, request, redirect, session, flash
from flask_socketio import SocketIO
from app import APP
import users
import moves
import templates
import trainingsessions
import likesandcomments
import notifications

socketio = SocketIO(APP)

@socketio.on("disconnect")
def disconnect_user():
    session.pop("username", None)
    session.pop("user_id", None)

@APP.route("/")
def index():
    followed_sessions = None
    liked_by_user = None
    users_notifs = None

    if session.get("user_id"):
        liked_by_user = likesandcomments.get_likes_by_user(session["user_id"])
        users_notifs = notifications.get_users_notifications(session["user_id"])

        if "max-date" in request.args and request.args["max-date"] != "":
            followed_sessions = trainingsessions.get_followed_sessions(
                session["user_id"], max_date=request.args["max-date"]
            )
        else:
            followed_sessions = trainingsessions.get_followed_sessions(session["user_id"])

    return render_template(
        "index.html",
        followed_sessions=followed_sessions,
        liked_by_user=liked_by_user,
        users_notifs=users_notifs
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
            flash(
                f"Registration unsuccessful - username {username} already taken.",
                "alert alert-danger"
            )
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

@APP.route("/userdata", methods=["GET"])
def userdata():
    if not session.get("user_id"):
        return redirect("/")

    userlist = users.get_userlist_with_followinfo(session["user_id"])

    return render_template("userdata.html", users=userlist)

@APP.route("/trainingsession/<int:id_>", methods=["GET"])
def get_trainingsessions(id_):
    if not session.get("user_id"):
        return redirect("/")

    session_data = trainingsessions.get_session_data(session["user_id"], id_)

    if session_data:
        session_comments = likesandcomments.get_comments(id_)
        main_info = {
            "session_id": id_,
            "username": session_data[0].username,
            "created_at": session_data[0].created_at,
            "likes": session_data[0].likes,
            "liked_by_current_user": session_data[0].liked_by_current_user
        }
        return render_template(
            "trainingsession.html",
            sessions=session_data,
            comments=session_comments,
            main_info=main_info
        )

    flash(
        f"No session with id {id_} found. \
        Either session {id_} does not exist, or its creator has disabled following.",
        "alert alert-danger"
    )
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

@APP.route("/addmove", methods=["GET", "POST"])
def add_move():
    if request.method == "POST":
        move_name = request.form["movename"]
        user_id = session["user_id"]

        if not moves.add_move(move_name, user_id):
            flash(
                f"Could not add new move {move_name}. Move names need to be unique.",
                "alert alert-danger"
            )
            return redirect("/moveslibrary")

        flash(f"New move {move_name} successfully added!", "alert alert-success")
    return redirect("/moveslibrary")

@APP.route("/deletemove/<int:id_>", methods=["GET", "POST"])
def delete_move(id_):
    if request.method == "POST":
        if moves.get_move_owner(id_) == session["user_id"]:
            moves.delete_move(id_)
            flash(f"Move {id_} deleted!", "alert alert-success")
        else:
            flash("You can only delete moves you have added yourself.", "alert alert-danger")

    return redirect("/moveslibrary")

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
    allow_follow_value = bool(users.get_allow_follow(session["username"]))

    if (request.method == "POST" and "allow-follow" in request.form):
        users.update_user(session["username"], request.form["allow-follow"])
        flash("Allow_follow successfully updated!", "alert alert-success")
        allow_follow_value = request.form["allow-follow"].lower() == "true"

    return render_template(
        "profile.html",
        allow_follow_value=allow_follow_value,
        moves=render_moves,
        users_templates=my_templates,
        complete_templates=complete_templates
    )

@APP.route("/trainingdata", methods=["GET"])
def trainingdata():
    if not session.get("user_id"):
        return redirect("/")

    users_sessions = trainingsessions.get_recent_sessions(session["user_id"])

    # Moves, templates and max weights need to be handled differently,
    # since they need to be JSON serializable.
    all_moves = moves.get_moves()
    moves_result = []

    for row in all_moves:
        moves_result.append(dict(row))

    users_templates = templates.get_users_templates(session["user_id"])
    all_templates = []

    for row in users_templates:
        all_templates.append(dict(row))

    recent_max = trainingsessions.get_recent_max_weights(session["user_id"])
    max_weights = []

    for row in recent_max:
        max_weights.append(dict(row))

    return render_template(
        "trainingdata.html",
        data_view_moves=moves_result,
        templates=all_templates,
        sessions=users_sessions,
        max_weights=max_weights
    )

@APP.route("/addtrainingsession", methods=["GET", "POST"])
def add_training_session():
    # https://stackoverflow.com/questions/50146815/getting-multiple-html-fields-with-same-name-using-getlist-with-flask-in-python
    if request.method == "POST":
        user_id = session["user_id"]
        submitted_move_list = request.form.getlist("selected-moves")
        submitted_reps_list = request.form.getlist("reps")
        submitted_weights_list = request.form.getlist("weights")

        if (len(submitted_move_list) == 0
            or len(submitted_reps_list) == 0
            or len(submitted_weights_list) == 0):
            flash(
                "Information regarding selected moves, reps or weights is missing.",
                "alert alert-danger"
            )
            return redirect(request.referrer)

        session_id = trainingsessions.add_training_session(user_id)

        if isinstance(session_id, int):
            for move, reps, weights in zip(submitted_move_list,
            submitted_reps_list, submitted_weights_list):
                trainingsessions.add_set(user_id, session_id, move, reps, weights)

            trainingsessions.complete_session(session_id)
            flash("Training session successfully saved!", "alert alert-success")
        else:
            flash("Could not create new training session.", "alert alert-danger")

    return redirect("/trainingdata")

@APP.route("/createtemplate", methods=["GET", "POST"])
def create_template():
    if request.method == "POST":
        creation_ret = templates.create_template(session["user_id"], request.form["template-name"])
        if isinstance(creation_ret, int):
            # Get selected move ids as list.
            selected_moves = request.form.getlist("selected-move-id")
            sets = request.form.getlist("sets")

            if (len(selected_moves) == 0 or len(sets) == 0):
                flash(
                    "Information regarding selected moves or number of sets is missing.",
                    "alert alert-danger"
                )
                return redirect("/profile")

            for move_id, number_of_sets in zip(selected_moves, sets):
                templates.add_to_reference_table(creation_ret, int(move_id), number_of_sets)
            flash("Template saved successfully!", "alert alert-success")
        else:
            flash("Could not create new template.", "alert alert-danger")

    return redirect("/profile")

@APP.route("/deletetemplate/<int:id_>", methods=["GET", "POST"])
def delete_template(id_):
    if request.method == "POST":
        if templates.get_template_owner(id_) == session["user_id"]:
            templates.delete_template(id_)
            flash(f"Template {id_} deleted!", "alert alert-success")
        else:
            flash("You can only delete your own training templates.", "alert alert-danger")

    return redirect("/profile")

@APP.route("/followunfollow/<int:id_>", methods=["GET", "POST"])
def follow_unfollow(id_):
    if request.method == "POST":
        follow = "follow" in request.form
        users.follow_unfollow(session["user_id"], id_, follow)
        flash(f"Follow information successfully updated for user {id_}.", "alert alert-success")

    return redirect("/userdata")

@APP.route("/like/<int:id_>", methods=["GET", "POST"])
def toggle_like(id_):
    if request.method == "POST":
        like = "like" in request.form

        if like:
            like_id = likesandcomments.like(id_, session["user_id"])
            session_owner = trainingsessions.get_session_owner(id_)
            if isinstance(like_id, int) and session_owner != session["user_id"]:
                notifications.create_notification(like_id)
        else:
            likesandcomments.remove_like(id_, session["user_id"])

    return redirect(request.referrer)

@APP.route("/addcomment/<int:id_>", methods=["GET", "POST"])
def add_comment(id_):
    if request.method == "POST":
        content = request.form["comment-text"]
        comment_id = likesandcomments.add_comment(session["user_id"], id_, content)

        if isinstance(comment_id, int):
            if trainingsessions.get_session_owner(id_) != session["user_id"]:
                notifications.create_notification(comment_id)
            flash("Comment added!", "alert alert-success")
        else:
            flash("Could not add new comment.", "alert alert-danger")

    return redirect(f"/trainingsession/{id_}")

@APP.route("/removecomment/<int:id_>", methods=["GET", "POST"])
def remove_comment(id_):
    related_session_id = likesandcomments.get_related_session(id_)

    if request.method == "POST":
        if likesandcomments.get_action_owner(id_) == session["user_id"]:
            likesandcomments.remove_comment(id_, session["user_id"])
            flash("You deleted your comment successfully!", "alert alert-success")
        else:
            flash("You can only delete your own comments.", "alert alert-danger")

    return redirect(f"/trainingsession/{related_session_id}")

@APP.route("/markasseen/<int:id_>", methods=["GET", "POST"])
def mark_as_seen(id_):
    if request.method == "POST":
        if notifications.get_notiftarget_owner(id_) == session["user_id"]:
            notifications.mark_as_seen(id_)
        else:
            flash("You can only mark notifications as seen \
                if they are related to your own training sessions.",
                "alert alert-danger")

    return redirect("/")
