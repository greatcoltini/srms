import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash


# CONSTANT FOR GRADES
GRADES = ['A', 'B', 'C', 'D', 'F']

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///management.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



@app.route("/")
def index():

    # init databases for info
    students = db.execute("SELECT * FROM students ORDER BY ID DESC")
    courses = db.execute("SELECT * FROM courses ORDER BY ID DESC")
    grades = db.execute("SELECT * FROM grades ORDER BY ID DESC")

    if not students or not courses or not grades:
        totalStudents = students[0]["ID"]
        totalCourses = courses[0]["ID"]
        totalGrades = grades[0]["ID"]

    # checks for no input to prevent weird none state
    if totalStudents == None:
        totalStudents = 0
    if totalCourses == None:
        totalCourses = 0
    if totalGrades == None:
        totalGrades = 0



    return render_template("index.html", courseTotal = totalCourses, studentTotal = totalStudents, gradesTotal = totalGrades)



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    """Log user in"""

    students = db.execute("SELECT * FROM students ORDER BY ID ASC")


    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # pull attributes from the form
        firstname = request.form.get("firstname")

        lastname = request.form.get("lastname")

        birthdate = request.form.get("birthdate")

        existing_students = db.execute("SELECT firstname, lastname FROM STUDENTS")

        for student in existing_students:
            if student["firstname"] == firstname and student["lastname"] == lastname:
                return flash("current student already present in database", "warning")

        # Insert user into database
        db.execute("INSERT INTO students (firstname, lastname, birthdate) VALUES (?, ?, ?)", firstname, lastname, birthdate)

        # notify user that the student was registered
        flash("Student " + firstname + " " + lastname + " has been registered.")

        students = db.execute("SELECT * FROM students ORDER BY ID ASC")

        # Redirect user to home page
        return render_template("student.html", students=students)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("student.html", students=students)
    

@app.route("/courses", methods=["GET", "POST"])
def courses():
    """Register user"""
    """Log user in"""

    courses = db.execute("SELECT * FROM courses ORDER BY coursename DESC")

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        coursename = request.form.get("coursename")

        existing_courses = db.execute("SELECT coursename FROM COURSES")

        for course in existing_courses:
            if course["coursename"] == coursename:
                flash("Course is already in the database.", "warning")
                return render_template("courses.html")

        # Insert user into database
        db.execute("INSERT INTO COURSES (coursename) VALUES (?)", coursename)

        flash("Course " + coursename + " has been added to the registry.")

        # Recalls the courses to add the newly added course
        courses = db.execute("SELECT * FROM courses ORDER BY coursename DESC")

        # Redirect user to home page
        return render_template("courses.html", courses=courses)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("courses.html", courses=courses)
    
@app.route("/results", methods=["GET", "POST"])
def results():
    """ method for launching the results page"""

    courses = db.execute("SELECT coursename FROM COURSES")
    students = db.execute("SELECT * FROM students") 
    gradetable = db.execute("SELECT * FROM grades ORDER BY coursename DESC, grade ASC")

    # user reached route via post, i.e. submitting the form
    if request.method == "POST":
        

        # grab variables from the form
        coursename = request.form.get("course")
        studentid = request.form.get("student")
        grade = request.form.get("grade")


        required_student = db.execute("SELECT * FROM students WHERE ID=%s", studentid)

        db.execute("INSERT INTO grades (coursename, firstname, lastname, grade) VALUES (?, ?, ?, ?)", 
                   coursename, required_student[0]['firstname'], required_student[0]['lastname'], grade)
        
        db.execute("UPDATE courses SET enrolled = enrolled + 1 WHERE coursename=%s", coursename)
        
        # flash user
        flash("Grades added to " + coursename + " from Student " + required_student[0]["firstname"])
        
        # refresh table upon add
        gradetable = db.execute("SELECT * FROM grades ORDER BY coursename DESC, grade DESC")


        return render_template("results.html", students = students, courses = courses, grades=GRADES, gradetable=gradetable)


    # user reached via get -- clicking link or redirct
    else:
        return render_template("results.html", students=students, courses=courses, grades=GRADES, gradetable=gradetable)

           

