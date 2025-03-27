from datetime import datetime, timedelta


class Reminder:
    def __init__(self, course_id, assignment_id, due_date, reminder_time):
        self.course_id = course_id
        self.assignment_id = assignment_id
        self.due_date = due_date
        self.reminder_time = reminder_time

    def get_upcoming_reminders(self, present_time=datetime.now()):
        # Calculate the time to send the reminder
        reminder_time = self.due_date - timedelta(hours=self.reminder_time)

        # If current time is equal or greater than reminder time, it's time to send a reminder
        if present_time >= reminder_time:
            return True
        return False

    def send_reminder(self):
        print(f"Reminder for Assignment {self.assignment_id} in Course {self.course_id}: "
              f"Due on {self.due_date.strftime('%Y-%m-%d %H:%M:%S')}")

    def add_reminder(self, reminders_list):
        reminders_list.append(self)

    def delete_reminder(self, reminders_list):
        reminders_list.remove(self)

reminders = []

def add_reminder(course_id, assignment_id, due_date, reminder_time):
    schedule_reminder = Reminder(course_id, assignment_id, due_date, reminder_time)
    schedule_reminder.add_reminder(reminders)

def check_and_send_reminders():
    time_now = datetime.now()
    for assignment_reminder in reminders:
        if assignment_reminder.get_upcoming_reminders(time_now):
            assignment_reminder.send_reminder()
            # Optionally delete reminder after sending
            assignment_reminder.delete_reminder(reminders)

# Adding a new reminder for an assignment
reminder = Reminder(course_id=202, assignment_id=202, due_date=datetime(2025, 4, 1, 12, 0), reminder_time=24)
reminder.add_reminder(reminders)

# Checking reminders (if the current time is 24 hours before the due date, it will send)
current_time = datetime(2025, 3, 31, 12, 0)  # Example of current time
for reminder in reminders:
    if reminder.get_upcoming_reminders(current_time):
        reminder.send_reminder()


