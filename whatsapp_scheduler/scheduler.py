import json
from datetime import datetime, timedelta

class MessageScheduler:
    def __init__(self, schedule_file):
        self.schedule_file = schedule_file
        self.schedules = self.load_schedules()

    def load_schedules(self):
        try:
            with open(self.schedule_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_schedules(self):
        with open(self.schedule_file, "w") as file:
            json.dump(self.schedules, file, indent=4)

    def add_message_schedule(self, contact, message, time, recurring):
        self.schedules.append({
            "type": "message",
            "contact": contact,
            "message": message,
            "time": time,
            "recurring": recurring,
            "sent": False
        })
        self.save_schedules()

    def add_poll_schedule(self, contact, question, options, time, recurring):
        self.schedules.append({
            "type": "poll",
            "contact": contact,
            "question": question,
            "options": options,
            "time": time,
            "recurring": recurring,
            "sent": False
        })
        self.save_schedules()

    def list_schedules(self):
        return self.schedules

    def remove_schedule(self, index):
        if 0 <= index < len(self.schedules):
            self.schedules.pop(index)
            self.save_schedules()

    def get_due_schedules(self, now):
        # Reload schedules from the JSON file to ensure the latest updates are reflected
        self.schedules = self.load_schedules()
        due_schedules = []
        for schedule in self.schedules:
            schedule_time = datetime.strptime(schedule["time"], "%d/%m/%Y %H:%M")
            if not schedule["sent"] and schedule_time <= now:
                due_schedules.append(schedule)
        return due_schedules

    def mark_as_sent(self, schedule):
        schedule["sent"] = True
        if schedule["recurring"]:
            schedule_time = datetime.strptime(schedule["time"], "%d/%m/%Y %H:%M")
            if schedule["recurring"] == "daily":
                schedule["time"] = (schedule_time + timedelta(days=1)).strftime("%d/%m/%Y %H:%M")
            elif schedule["recurring"] == "weekly":
                schedule["time"] = (schedule_time + timedelta(weeks=1)).strftime("%d/%m/%Y %H:%M")
            elif schedule["recurring"] == "monthly":
                schedule["time"] = (schedule_time + timedelta(days=30)).strftime("%d/%m/%Y %H:%M")
            schedule["sent"] = False
        self.save_schedules()