import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///management.db")

# Make sure API key is set
# if not os.environ.get("API_KEY"):
#     raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



@app.route("/")
def index():

    return render_template("index.html")



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure first name was submitted
        if not request.form.get("firstname"):
            return apology("must provide your first name", 400)

        # Ensure last name was submitted
        elif not request.form.get("lastname"):
            return apology("must provide your last name", 400)
        

        firstname = request.form.get("firstname")

        lastname = request.form.get("lastname")

        birthdate = request.form.get("birthdate")

        existing_students = db.execute("SELECT firstname FROM STUDENTS")

        for student in existing_students:
            if student["firstname"] == firstname and student["lastname"] == lastname:
                return apology("current student already present in database")

        # Insert user into database
        db.execute("INSERT INTO students (firstname, lastname, birthdate) VALUES (?, ?, ?)", firstname, lastname, birthdate)

        # notify user that the student was registered
        flash("Student " + firstname + " " + lastname + " has been registered.")

        # Redirect user to home page
        return render_template("student.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("student.html")
    

@app.route("/courses", methods=["GET", "POST"])
def courses():
    """Register user"""
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("coursename"):
            return apology("must provide your course name", 400)
        
        coursename = request.form.get("coursename")

        existing_courses = db.execute("SELECT coursename FROM COURSES")

        for course in existing_courses:
            if course["coursename"] == coursename:
                return apology("current course already present in database")

        # Insert user into database
        db.execute("INSERT INTO COURSES (coursename) VALUES (?)", coursename)

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("courses.html")

