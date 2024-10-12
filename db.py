import sqlite3
from datetime import datetime


class Database:
    def __init__(self, db_name='main.db'):
        """Initializing a database connection and create tables if they don't exist."""
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        """Create tables for storing habits and tracking."""
        self.conn.execute("""CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT, 
            description TEXT,
            periodicity TEXT, 
            creation_date DATE) 
        """)

        self.conn.execute("""CREATE TABLE IF NOT EXISTS tracking (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER,
            checkoff_date DATE, 
            FOREIGN KEY (habit_id) REFERENCES habits(id))
        """)
        self.conn.commit()

    def check_habit_exists(self, name):
        """Have a look if a habit with the given name already exists in the habits table."""
        cursor = self.conn.execute("SELECT id FROM habits WHERE LOWER(name) = ?", (name.lower(),))
        result = cursor.fetchone()
        return result is not None

    def add_habit_to_table(self, habit):
        """How to save a habit in the database."""
        self.conn.execute("INSERT INTO habits (name, description, periodicity, creation_date) VALUES (?, ?, ?, ?)",
                          (habit.get_name(), habit.get_description(), habit.get_periodicity(),
                          habit.get_creation_date().strftime("%Y-%m-%d %H:%M:%S")))
        habit_id = self.conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        self.conn.commit()
        return habit_id

    def delete_habit_from_table(self, habit_id):
        """How to delete a habit and its checkoff dates from the tables."""
        self.conn.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
        self.conn.execute("DELETE FROM tracking WHERE habit_id = ?", (habit_id,))
        self.conn.commit()

    def add_streak_to_table(self, habit_id, checkoff_date):
        """How to save checkoff dates to the tracking table."""
        self.conn.execute("INSERT INTO tracking (habit_id, checkoff_date) VALUES (?, ?)",
                          (habit_id, checkoff_date.strftime("%Y-%m-%d %H:%M:%S")))
        self.conn.commit()

    def update_habit_in_table(self, habit_id, new_name, new_description):
        """How to  save updated habit names and/or descriptions in the habits table."""
        self.conn.execute("UPDATE habits SET name = ?, description = ?"
                          "WHERE id = ?", (new_name, new_description, habit_id))
        self.conn.commit()

    def get_all_habits(self):
        """How to get all stored habits with their checkoff dates."""
        habits = []
        cursor = self.conn.execute("SELECT id, name, description, periodicity, creation_date FROM habits")
        habit_data = cursor.fetchall()
        for row in habit_data:
            habit_id = row[0]
            habit = {
                'id': habit_id,
                'name': row[1],
                'description': row[2],
                'periodicity': row[3],
                'creation_date': row[4],
                'checkoff_dates': self.get_all_checkoff_dates(habit_id)
            }
            habits.append(habit)
        return habits

    def get_all_checkoff_dates(self, habit_id):
        """Retrieve all stored checkoff dates from one habit."""
        cursor = self.conn.execute("SELECT checkoff_date FROM tracking WHERE habit_id = ?", (habit_id,))

        checkoff_dates = []
        for row in cursor.fetchall():
            date_str = row[0]
            try: # First try parsing the full date-time format
                checkoff_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            except ValueError: # If it fails, try parsing just the date part
                checkoff_date = datetime.strptime(date_str, "%Y-%m-%d")

            checkoff_dates.append(checkoff_date)

        return checkoff_dates

    def get_habit_id(self, name):
        """How to get a stored habit by ID when only name is given."""
        cursor = self.conn.execute("SELECT id FROM habits WHERE LOWER(name) = LOWER(?)", (name,))
        result = cursor.fetchone()
        return result[0] if result else None