from habit import Habit
from db import Database


class Analyse:
    def __init__(self, db):
        """Initialize the Analyse class with a Database instance."""
        self.db = db

    def get_all_stored_habits(self):
        """Retrieve a list of all stored habit names, regardless of their checkoff dates"""
        habits = self.db.get_all_habits()
        all_habits = [habit['name'] for habit in habits]
        return all_habits

    def get_all_checked_off_habits(self):
        """Retrieve a list of habit names that have at least one tracked checkoff date."""
        habits = self.db.get_all_habits()
        tracked_habits = [habit['name'] for habit in habits if habit['checkoff_dates']]
        return tracked_habits

    def get_habits_by_periodicity(self, periodicity):
        """Retrieve two lists of habit names based on the specified periodicity:
        - One list contains habits with checkoff dates.
        - The other list contains habits without checkoff dates.
        """
        habits = self.db.get_all_habits()

        with_checkoff = [habit['name'] for habit in habits if habit['periodicity'] == periodicity
                         and habit['checkoff_dates']]
        without_checkoff = [habit['name'] for habit in habits if habit['periodicity'] == periodicity
                            and not habit['checkoff_dates']]

        return with_checkoff, without_checkoff

    def get_longest_streak_daily(self):
        """Calculate the longest streak among all daily habits.

         Returns a tuple containing:
         - A list of habit names that have the longest streak.
         - The length of the longest streak.
        """
        habits = self.db.get_all_habits()
        longest_streak = 0
        habit_with_longest_streak = []

        for habit_data in habits:
            if habit_data["periodicity"] != "daily":
                continue # Means: Skip non-daily habits

            checkoff_dates = self.db.get_all_checkoff_dates(habit_data["id"])
            habit = Habit(habit_data["name"], habit_data["description"], habit_data["periodicity"])
            habit.checkoff_dates = checkoff_dates

            streak = habit.streak() # Calculate the current streak

            if streak > longest_streak:
                longest_streak = streak
                habit_with_longest_streak = [habit_data["name"]] # Reset list with this habit
            elif streak == longest_streak:
                habit_with_longest_streak.append(habit_data["name"]) # Add habit to the list

        return habit_with_longest_streak, longest_streak

    def get_longest_streak_weekly(self):
        """Calculate the longest streak among all weekly habits.

        Returns a tuple containing:
         - A list of habit names that have the longest streak.
         - The length of the longest streak.
        """
        habits = self.db.get_all_habits()
        longest_streak = 0
        habit_with_longest_streak = []

        for habit_data in habits:
            if habit_data["periodicity"] != "weekly":
                continue  # Means: Skip non-weekly habits

            checkoff_dates = self.db.get_all_checkoff_dates(habit_data["id"])
            habit = Habit(habit_data["name"], habit_data["description"], habit_data["periodicity"])
            habit.checkoff_dates = checkoff_dates

            streak = habit.streak()  # Calculate the current streak

            if streak > longest_streak:
                longest_streak = streak
                habit_with_longest_streak = [habit_data["name"]]  # Reset list with this habit
            elif streak == longest_streak:
                habit_with_longest_streak.append(habit_data["name"])  # Add habit to the list

        return habit_with_longest_streak, longest_streak

    def get_longest_streak_by_name(self, habit_name):
        """Calculate the longest streak for a specific habit identified by its name.

        Returns a tuple containing:
        - The habit name.
        - The length of the longest streak. If the habit is not found, returns None and 0.
        """
        habit_id = self.db.get_habit_id(habit_name)
        if habit_id is None:
            return None, 0 # Habit not found

        checkoff_dates = self.db.get_all_checkoff_dates(habit_id)
        habit_data = self.db.conn.execute("SELECT name, description, periodicity FROM habits WHERE id = ?",
                                          (habit_id,)).fetchone()
        if not habit_data:
            return None, 0 # Habit not found

        habit = Habit(habit_data[0], habit_data[1],habit_data[2])
        habit.checkoff_dates = checkoff_dates
        return habit_name, habit.streak() # Return the habit name and its streak