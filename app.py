import os

from flask import Flask, render_template, request, session, flash, url_for, redirect
from dotenv import load_dotenv
from datetime import datetime
from Reminder import add_reminder,reminders
from CourseEnrollment import CourseEnrollment

app = Flask(__name__, template_folder='templates')
app.secret_key = os.getenv('APP_SECRET_KEY')
load_dotenv()

# Instantiate CourseEnrollment class with the Canvas API details
CANVAS_BASE_URL = "https://bsu.instructure.com/api/v1"
API_TOKEN = os.getenv("API_KEY")
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
course_enrollment = CourseEnrollment(CANVAS_BASE_URL, API_TOKEN)

# Function to fetch current courses
@app.route('/courses')
def courses():
    # Fetch the current courses
    courses = course_enrollment.fetch_current_courses()
    return render_template('courses.html', courses=courses)

#Login for authenticated user
@app.route('/', methods=['GET', 'POST'])
def login():
    print(request.method)
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email == EMAIL and password == PASSWORD:
            session['user'] = email
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))
# Home route to fetch courses and reminders
@app.route('/home', methods=['GET', 'POST'])
def home():
    # Fetch current courses and reminders
    if 'user' not in session:
        return redirect(url_for('login'))

    courses = course_enrollment.fetch_current_courses()
    if courses:
        first_course_id = courses[0].get('id')
        assignments = course_enrollment.fetch_assignments(first_course_id)
    else:
        assignments = []
    return render_template('home.html', courses=courses, assignments=assignments)

# Route to fetch assignments for a specific course
@app.route('/course/<int:course_id>/assignments')
def course_assignments(course_id):
    assignments = course_enrollment.fetch_assignments(course_id)
    print(assignments)
    assignment_list = [{'name': assignment['name']} for assignment in assignments]
    return render_template('assignments.html', assignments=assignment_list)


# Route to add a new reminder (e.g., for a specific assignment)
@app.route('/add_reminder', methods=['POST'])
def add_new_reminder():
    # Assuming you get the data from the form
    course_name = request.form.get('course_name')
    assignment_name = request.form.get('assignment_name')
    due_date_str = request.form['due_date']
    reminder_time = int(request.form['reminder_time'])

    # Parse the due date from the form input (assuming it's in 'YYYY-MM-DD' format)
    due_date = datetime.strptime(due_date_str, '%Y-%m-%d')


    # Add the reminder
    add_reminder(course_name, assignment_name, due_date, reminder_time)

    return render_template('home.html', courses=course_enrollment.fetch_current_courses(), reminders=reminders)


# Route to view reminders (this will show all upcoming reminders)
@app.route('/reminders')
def view_reminders():
    return render_template('reminders.html', reminders=reminders)

@app.route('/assignments')
def fetch_assignments():
    # Example course and assignment data from Canvas API
    course_name = course_enrollment.fetch_current_courses()[0]['name']
    assignment_name = course_enrollment.fetch_assignments(course_name)[0]['name']
    due_date = datetime(2025, 4, 1, 12, 0)  # Due date for assignment
    reminder_time = 24  # Reminder 24 hours before due date
    assignments = course_enrollment.fetch_assignments(course_name)
    # Add the reminder
    add_reminder(course_name, assignment_name, due_date, reminder_time)

    return render_template('assignments.html', assignments=assignments)

if __name__ == "__main__":
    app.run(debug=True)