# PROJECT OUTLINE
- We will attempt to create a Single Page App for a Student Result Management System

# PROJECT SPECS

## Homepage
- we must have a homepage that links to the other pages;
    - links must be via a navigation bar on the left hand side
        - Home
        - Students
        - Courses
        - Results

## Students Page
- form with controls for submission to database
    - First Name
    - Family Name
    - Date of Birth
    - Submit
- upon submission, all controls must be filled
- date of birth must be valid date and student at least 10 years old

- once submitted, send notification and clear controls


- also have a tabular list of all students

## Courses Page
- submission form for courses

- has a tabular list of all courses; lets add in enrolled students

## Results Page
- submission form for grading of students
- contains list of all courses, list of all students, and list of grades to use




# PROJECT INSTALL AND RUNNING
1. NAVIGATE TO THE DIRECTORY
2. OPEN TERMINAL IN THE DIRECTORY
3. INSTALL THE DEPENDENCIES VIA THE FOLLOWING COMMAND:
pip install -r requirements.txt

4. RUN THE APPLICATION WITH TERMINAL IN THE DIRECTORY
python -m flask run

5. THE SERVER WILL NOW BE LOCALLY HOSTED ; NAVIGATE WITH YOUR PREFERRED WEB BROWSER TO WHATEVER YOUR LOCAL HOST WITH PORT 5000 DEFAULTS TO
For example, my local server was hosted on http://127.0.0.1:5000

So, once running the " python -m flask run " command, I will navigate to the above network address in Microsoft Edge.
