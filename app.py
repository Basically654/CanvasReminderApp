import os

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from Reminder import add_reminder, check_and_send_reminders, reminders  # Import reminder functions
from CourseEnrollment import CourseEnrollment  # Assuming this is already implemented

app = Flask(__name__, template_folder='templates')
load_dotenv()

# Instantiate CourseEnrollment class with the Canvas API details
CANVAS_BASE_URL = "https://bsu.instructure.com/api/v1"
API_TOKEN = os.getenv("API_KEY")
course_enrollment = CourseEnrollment(CANVAS_BASE_URL, API_TOKEN)



# Function to fetch current courses
@app.route('/courses')
def courses():
    # Fetch the current courses
    courses = course_enrollment.fetch_current_courses()
    return render_template('courses.html', courses=courses)


# Home route to fetch courses and reminders
@app.route('/')
def home():
    # Fetch current courses and reminders
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
    return jsonify(assignment_list)


# Route to add a new reminder (e.g., for a specific assignment)
@app.route('/add_reminder', methods=['POST'])
def add_new_reminder():
    # Assuming you get the data from the form
    course_name = request.form.get('course_id')
    assignment_name = request.form.get('assignment_name')
    due_date_str = request.form['due_date']
    reminder_time = int(request.form['reminder_time'])

    # Parse the due date from the form input (assuming it's in 'YYYY-MM-DD' format)
    due_date = datetime.strptime(due_date_str, '%B %d, %Y')


    # Add the reminder
    add_reminder(course_name, assignment_name, due_date, reminder_time)

    return render_template('home.html', courses=course_enrollment.fetch_current_courses(), reminders=reminders)


# Route to view reminders (this will show all upcoming reminders)
@app.route('/reminders')
def view_reminders():
    return render_template('reminders.html', reminders=reminders)

# Periodic task to check and send reminders
def scheduled_task():
    check_and_send_reminders()

# Initialize the scheduler and start it
scheduler = BackgroundScheduler()
scheduler.add_job(scheduled_task, 'interval', minutes=1)  # Check every minute
scheduler.start()

if __name__ == "__main__":
    app.run(debug=True)

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

@app.route('/reminders', methods=['GET'])
def view_reminders():
    # Show reminders to the user (you can customize this template)
    return render_template('reminders.html', reminders=reminders)

if __name__ == "__main__":
    app.run(debug=True)