from flask import Flask, flash, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app = Flask(__name__)

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# initialize the app with the extension
db.init_app(app)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.secret_key = "superior key"
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

@app.route("/")
def homepage():
    return render_template("index.html", title="HOME PAGE")

@app.route("/register", methods=["GET", "POST"])
def register():
    if 'username' in session:
        print("Your are logged in as ", session["username"])
        return
    print("You are not logged in")

    """Register user"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        print("POST")

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("must provide username")
            return render_template("register.html")

#         # Query database for username
#         rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

#         # Ensure username does not exist
#         if len(rows) != 0:
#             return apology("user already exists", 400)

#         # Ensure password was submitted
#         elif not request.form.get("password"):
#             return apology("must provide password", 400)

#         # Ensure password and confirmation are the same
#         elif request.form.get("password") != request.form.get("confirmation"):
#             return apology("passwords do not match", 400)

#         # add user to database
#         username = request.form.get("username")
#         hash = generate_password_hash(request.form.get("password"))

#         db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash)

#         # Log the newly registered user in
#         rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
#         session["user_id"] = rows[0]["id"]

#         # Redirect user to home page
        return redirect("/")
    else:
        print("GET")
        return render_template("register.html")

if __name__ == "__main__":
    app.run(debug=True)