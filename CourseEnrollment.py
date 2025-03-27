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
    def __init__(self, canvas_base_url, API_TOKEN):
        self.canvas_base_url = canvas_base_url
        self.headers = {
            "Authorization": f"Bearer {API_TOKEN}"
        }

    def fetch_current_courses(self):
        url = f"{self.canvas_base_url}/courses"
        params = {
            "enrollment_state": "active",
            "enrollment_term_id": "38",
            "enrollment_role": "StudentEnrollment"
        }
        try:
            # Use requests.get() with params as a dictionary
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()  # Ensure no HTTP errors occurred
            # Return the JSON response
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"Error occurred: {err}")
        return []

    def getURL(self, endpoint, **params):
        """
        Constructs the URL for the Canvas API endpoint.

        :param endpoint: The API endpoint (e.g., '/courses/{course_id}/assignments').
        :param params: Additional query parameters to append to the URL.
        :return: The full URL.
        """
        # Append the endpoint to the base URL
        full_url = f"{self.canvas_base_url}{endpoint}"

        # If there are additional query parameters, append them as a query string
        if params:
            query_string = "&".join([f"{key}={value}" for key, value in params.items()])
            full_url += f"?{query_string}"

        return full_url

    def fetch_assignments(self, course_id):
        # Use getURL to build the URL
        url = self.getURL(f"/courses/{course_id}/assignments")
        print(f"Fetching assignments from URL: {url}")
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()  # Check for HTTP errors
            assignments = response.json()

            assignment_list = []
            for assignment in assignments:
                assignment_data = {
                    "name" : assignment["name"],
                    "due_at" : assignment["due_at"],
                }
                assignment_list.append(assignment_data)

            return assignment_list
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"Error occurred: {err}")
        return []


if __name__ == '__main__':
    # Create an instance of the CourseEnrollment class
    course_enrollment = CourseEnrollment(CANVAS_BASE_URL, API_TOKEN)

    # Call the fetch_current_courses method on the instance
    print(course_enrollment.fetch_current_courses())