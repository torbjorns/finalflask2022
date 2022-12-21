"""Importing the needed modules"""
from flask import Flask, flash, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from helpers import create_connection, execute_query, execute_read_query

connection = create_connection("test.db")

create_users_table = """
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  hash TEXT NOT NULL
);
"""

execute_query(connection, create_users_table)

app = Flask(__name__)

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
    # rows = db.execute("SELECT * FROM tbl1")
    # print(rows)
    if 'username' in session:
        print("Your are logged in as ", session["username"])
        return
    print("You are not logged in")

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        print("POST")

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("You must provide a username")
            return render_template("register.html")

        connection = create_connection("test.db")

        new_query = ("SELECT * FROM users WHERE name = ", "'", request.form.get("username"), "'")
        get_username = "".join(new_query)
        user = execute_read_query(connection, get_username)

        # Ensure username does not exist
        if user:
            flash("There is a user")
            return render_template("register.html")
        else:
            flash("No such user")
            return render_template("register.html")

        # Ensure password was submitted
        if not request.form.get("password"):
            flash("You must provide a password")
            return render_template("register.html")

        # Ensure password and confirmation are the same
        if request.form.get("password") != request.form.get("confirmation"):
            flash("The two passwords are not the same")
            return render_template("register.html")

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