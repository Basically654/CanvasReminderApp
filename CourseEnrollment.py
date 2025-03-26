import requests
import os
from dotenv import load_dotenv

load_dotenv()
# Your Canvas API URL (replace with your Canvas domain)
CANVAS_BASE_URL = "https://bsu.instructure.com/api/v1"
# Replace with your API token
API_TOKEN = os.getenv("API_KEY")

# Define headers for authentication
headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}


# Function to fetch only current courses (active enrollments)
class CourseEnrollment:
    def __init__(self, canvas_base_url, api_token):
        self.canvas_base_url = canvas_base_url
        self.headers = {
            "Authorization": f"Bearer {api_token}"
        }

    def fetch_current_courses(self):
        url = f"{self.canvas_base_url}/courses"
        params = {
            "enrollment_state": "active",
            "enrollment_term_id": "38",  # Change to the term ID you're targeting (e.g., Spring 2025)
            "enrollment_role": "StudentEnrollment"
        }
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"Error occurred: {err}")
        return []

    def fetch_assignments(self, course_id):
        url = f"{self.canvas_base_url}/courses/{course_id}/assignments"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"Error occurred: {err}")
        return []