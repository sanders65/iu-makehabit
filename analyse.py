from habit import Habit
from db import Database


class Analyse:
    def __init__(self, db_name='main.db'):
        self.db = Database(db_name)

    def get_all_stored_habits(self):
        """Returns a list of all habits with and without checkoff dates"""
        habits = self.db.get_all_habits()
        all_habits = [habit['name'] for habit in habits]
        return all_habits

    def get_all_checked_off_habits(self):
        """Returns a list of habits with at least one checkoff date."""
        habits = self.db.get_all_habits()
        tracked_habits = [habit['name'] for habit in habits if habit['checkoff_dates']]
        return tracked_habits

    def get_habits_by_periodicity(self, periodicity):
        """Returns two lists of habits with their given periodicity,
            one with checkoff dates, one without checkoff dates."""
        habits = self.db.get_all_habits()

        with_checkoff = [habit['name'] for habit in habits if habit['periodicity'] == periodicity
                         and habit['checkoff_dates']]
        without_checkoff = [habit['name'] for habit in habits if habit['periodicity'] == periodicity
                            and not habit['checkoff_dates']]

        return with_checkoff, without_checkoff

    def get_longest_streak_daily(self):
        """Returns the longest streak of all daily habits and the streak length"""
        habits = self.db.get_all_habits()
        longest_streak = 0
        habit_with_longest_streak = []

        for habit_data in habits:
            if habit_data["periodicity"] != "daily":
                continue # means: skip non-daily habits

            checkoff_dates = self.db.get_all_checkoff_dates(habit_data["id"])
            habit = Habit(habit_data["name"], habit_data["description"], habit_data["periodicity"])
            habit.checkoff_dates = checkoff_dates

            streak = habit.streak() # Calculate streak

            if streak > longest_streak:
                longest_streak = streak
                habit_with_longest_streak = [habit_data["name"]] # Reset list with this habit
            elif streak == longest_streak:
                habit_with_longest_streak.append(habit_data["name"]) # Add habit to list

        return habit_with_longest_streak, longest_streak

    def get_longest_streak_weekly(self):
        """Returns the longest streak of all weekly habits"""
        habits = self.db.get_all_habits()
        longest_streak = 0
        habit_with_longest_streak = []

        for habit_data in habits:
            if habit_data["periodicity"] != "weekly":
                continue  # means: skip non-weekly habits

            checkoff_dates = self.db.get_all_checkoff_dates(habit_data["id"])
            habit = Habit(habit_data["name"], habit_data["description"], habit_data["periodicity"])
            habit.checkoff_dates = checkoff_dates

            streak = habit.streak()  # Calculate streak

            if streak > longest_streak:
                longest_streak = streak
                habit_with_longest_streak = [habit_data["name"]]  # Reset list with this habit
            elif streak == longest_streak:
                habit_with_longest_streak.append(habit_data["name"])  # Add habit to list

        return habit_with_longest_streak, longest_streak

    def get_longest_streak_by_name(self, habit_name):
        """Returns the longest streak for a specific habit."""
        habit_id = self.db.get_habit_id(habit_name)
        if habit_id is None:
            return None, 0 # If habit can not be found

        checkoff_dates = self.db.get_all_checkoff_dates(habit_id)
        habit_data = self.db.conn.execute("SELECT name, description, periodicity FROM habits WHERE id = ?",
                                          (habit_id,)).fetchone()
        if not habit_data:
            return None, 0

        habit = Habit(habit_data[0], habit_data[1],habit_data[2])
        habit.checkoff_dates = checkoff_dates
        return habit_name, habit.streak()