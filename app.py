from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request
from flask_session import Session


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


"""
Default route for user to take; contains the landing page for the user.

This route will provide information about the student, grades, and course count.
Because of this, we must pull this information from the database, if there is no
count for any of these values then we pass.

"""
@app.route("/")
def index():

    # init variables
    totalStudents = None 
    totalCourses = None 
    totalGrades = None

    # init databases for info
    students = db.execute("SELECT COUNT(*) FROM students")
    courses = db.execute("SELECT COUNT(*) FROM courses")
    grades = db.execute("SELECT COUNT(*) FROM grades")

    if not students or not courses or not grades:
        pass
    else:
        totalStudents = students[0]['COUNT(*)']
        totalCourses = courses[0]['COUNT(*)']
        totalGrades = grades[0]['COUNT(*)']

    # checks for no input to prevent weird none state
    if totalStudents == None:
        totalStudents = 0
    if totalCourses == None:
        totalCourses = 0
    if totalGrades == None:
        totalGrades = 0



    return render_template("index.html", courseTotal = totalCourses, studentTotal = totalStudents, gradesTotal = totalGrades)



"""
The student registration page.

Methods:

POST: The user reaches this via submitting a form. This is the stage where a 
user will be registering a student. We will pull the student's information
via the form submission, and fill in the database correspondingly.

GET: The user got to this page by redirect or another link; this is the default
possibility for the user, no form submission methods needed.

When we render this page we need to pass in the students table to
display the HTML view of the students.

"""
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
                flash("current student already present in database", "warning")
                return render_template("student.html", students=students)

        # Insert user into database
        db.execute("INSERT INTO students (firstname, lastname, birthdate) VALUES (?, ?, ?)", firstname, lastname, birthdate)

        # notify user that the student was registered
        flash("Student " + firstname + " " + lastname + " has been registered.", category="primary")

        students = db.execute("SELECT * FROM students ORDER BY ID ASC")

        # Redirect user to home page
        return render_template("student.html", students=students)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("student.html", students=students)
    

"""
The course registration page.

POST: The user reaches this page via submitting the course form. This is the
point where the user will be registering a course for the database.
This is straightforward, and will just fill in a new item on the course 
table in the database.

GET: The user got to this page via redirect or another link; no action required.

When we render this template we need to pass in the courses table to render the
HTML viewing of the table.

"""
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
                return render_template("courses.html", courses=courses)

        # Insert user into database
        db.execute("INSERT INTO COURSES (coursename) VALUES (?)", coursename)

        flash("Course " + coursename + " has been added to the registry.", category="primary")

        # Recalls the courses to add the newly added course
        courses = db.execute("SELECT * FROM courses ORDER BY coursename DESC")

        # Redirect user to home page
        return render_template("courses.html", courses=courses)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("courses.html", courses=courses)
    

"""
The grading page for the students.

POST: In the post section, we will add a new item to the grades table
corresponding to the student's grade with the corresponding course.

GET: As with the other methods, we get here via link and therefore just
display the page.

Whenever we render this template, we need to pass in the three
tables to generate the form fields and the table below.

"""
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

        student_fn = required_student[0]['firstname']
        student_ln = required_student[0]['lastname']

        if not db.execute("SELECT * FROM grades "
                    + "WHERE firstname=%s AND lastname=%s AND coursename=%s", student_fn,
                    student_ln, coursename):
            db.execute("INSERT INTO grades (coursename, firstname, lastname, grade) VALUES (?, ?, ?, ?)", 
                    coursename, student_fn, student_ln, grade)
            
            db.execute("UPDATE courses SET enrolled = enrolled + 1 WHERE coursename=%s", coursename)
        
            # flash user
            flash("Grades added to " + coursename + " from Student " + student_fn + " " + student_ln, category="primary")
        else:
            flash("Student " + student_fn + " " + student_ln + " is already enrolled in course " + coursename, category="warning")
        
        # refresh table upon add
        gradetable = db.execute("SELECT * FROM grades ORDER BY coursename DESC, grade DESC")


        return render_template("results.html", students = students, courses = courses, grades=GRADES, gradetable=gradetable)


    # user reached via get -- clicking link or redirct
    else:
        return render_template("results.html", students=students, courses=courses, grades=GRADES, gradetable=gradetable)

           

