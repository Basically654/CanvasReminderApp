import os

from dotenv import load_dotenv
from flask import Flask, render_template
from CourseEnrollment import CourseEnrollment  # Import your class

app = Flask(__name__, template_folder='templates')
load_dotenv()

# Instantiate CourseEnrollment class with the Canvas API details
CANVAS_BASE_URL = "https://canvas.instructure.com/api/v1"
API_TOKEN = os.getenv("API_KEY")
course_enrollment = CourseEnrollment(CANVAS_BASE_URL, API_TOKEN)



@app.route('/courses')
def courses():
    # Fetch the current courses
    course_enrollment = CourseEnrollment(CANVAS_BASE_URL, API_TOKEN)
    courses = course_enrollment.fetch_current_courses()
    return render_template('courses.html', courses=courses)
@app.route('/')
def home():
    # Fetch the current courses
    courses = course_enrollment.fetch_current_courses()  # Call the function here
    # Pass the courses to the template
    return render_template('home.html', courses=courses)
@app.route('/course/<int:course_id>/assignments')
def course_assignments(course_id):
    assignments = course_enrollment.fetch_assignments(course_id)
    return render_template('assignments.html', assignments=assignments)

if __name__ == "__main__":
    app.run(debug=True)