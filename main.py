"""Importing the needed modules"""
from flask import Flask, flash, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from sqlite3 import Error

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

connection = create_connection("test.db")

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

create_users_table = """
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  age INTEGER,
  gender TEXT,
  nationality TEXT
);
"""

execute_query(connection, create_users_table)

create_users = """
INSERT INTO
  users (name, age, gender, nationality)
VALUES
  ('James', 25, 'male', 'USA'),
  ('Leila', 32, 'female', 'France'),
  ('Brigitte', 35, 'female', 'England'),
  ('Mike', 40, 'male', 'Denmark'),
  ('Elizabeth', 21, 'female', 'Canada');
"""

execute_query(connection, create_users)

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The erros '{e}' occurred")

select_users = "SELECT * from users"
users = execute_read_query(connection, select_users)

for user in users:
    print(user)


db = SQLAlchemy()

app = Flask(__name__)

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
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

#         # Query database for username
#         rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

#         # Ensure username does not exist
#         if len(rows) != 0:
#             return apology("user already exists", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("You must provide a password")
            return render_template("register.html")

        # Ensure password and confirmation are the same
        elif request.form.get("password") != request.form.get("confirmation"):
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