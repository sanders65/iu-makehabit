from datetime import date
from db import add_habit_data, add_tracking_data


class Habit:
    def __init__(self, name: str, periodicity: str):
        """Some text ..."""
        self.name = name
        self.periodicity = periodicity
        self.creation_date = date.today()
        self.streak = 0

    def __str__(self):
        return f"{self.name}, {self.periodicity}, {self.creation_date}, {self.streak}"

    def periodicity(self):
        self.periodicity = ["daily", "weekly"]

    def store_habit_data(self, db):
        add_habit_data(db, self.name, self.periodicity, self.creation_date, self.streak)


class Streak:
    def __init__(self, name: str, checkoff_date: date.today(), streak: int):
        self.name = name
        self.checkoff_date = checkoff_date
        self.streak = streak

    def __str__(self):
        return f"{self.name}, {self.checkoff_date}, {self.streak}"

    def streak_raise(self):
        self.streak_raise += 1

    def streak_break(self):
        self.streak_break = 0

    def store_tracking_data(self, db):
        add_tracking_data(db, self.name, self.checkoff_date, self.streak)