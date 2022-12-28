from flask import Flask
from flask import render_template, request, redirect, session
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
            return render_template("register.html", errormessage="Password fields do not match.")

        if users.register_user(username, password1):
            return redirect("/")
        else:
            return render_template("register.html", errormessage="Registration unsuccessful.")


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
            return redirect("/register")

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
    allow_follow_value = users.get_allow_follow(session["username"])[0]

    if request.method == "GET":
        return render_template("profile.html", allow_follow_value=allow_follow_value)
    
    if request.method == "POST" and "allow_follow" in request.form:
        success = users.update_user(session["username"], request.form["allow_follow"])
        allow_follow_value = request.form["allow_follow"]
        if not success:
            return render_template("profile.html", errormessage="Could not update allow_follow.")

    return render_template("profile.html", allow_follow_value=allow_follow_value)    
        

