from flask import Flask
from flask import render_template, request, redirect, session, flash
from os import getenv


app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
import users
import moves

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
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

        if users.register_user(username, password1):
            return redirect("/")
        else:
            flash("Registration unsuccessful.", "alert alert-danger")
            return redirect("/register")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        all_users = users.get_users()
        return render_template("index.html", users=all_users)
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            flash("Login unsuccessful - check username and password.", "alert alert-danger")
            return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    del session["user_id"]
    return redirect("/")

@app.route("/moveslibrary")
def moveslibrary():
    render_moves = ""

    if "query" in request.args:
        query = request.args["query"]
        render_moves = moves.search_moves(query)
    else:
        render_moves = moves.get_moves()

    return render_template("moveslibrary.html", moves=render_moves)

@app.route("/profile", methods=["GET", "POST"])
def profile():
    # Get current value from database.
    allow_follow_value = bool(users.get_allow_follow(session["username"])[0])
    
    if request.method == "GET":
        return render_template("profile.html", allow_follow_value=allow_follow_value)
    
    if request.method == "POST" and "allow_follow" in request.form:
        success = users.update_user(session["username"], request.form["allow_follow"])

        if not success:
            flash("Could not update allow_follow.", "alert alert-danger")
            return render_template("profile.html")
        else:
            flash("Allow_follow successfully updated!", "alert alert-success")
            allow_follow_value = request.form["allow_follow"].lower() == "true"

            return render_template("profile.html", allow_follow_value=allow_follow_value)

@app.route("/addmove", methods=["POST"])
def add_move():
    move_name = request.form["movename"]

    if not moves.add_move(move_name):
        flash(f"Could not add new move {move_name}.", "alert alert-danger")
        return redirect("/moveslibrary")

    flash(f"New move {move_name} successfully added!", "alert alert-success")
    return redirect("/moveslibrary")
