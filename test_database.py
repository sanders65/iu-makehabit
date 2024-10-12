import pytest
from habit import Habit
from db import Database
from datetime import datetime


# Test suite for database-related functionality
class TestDatabase:

    # Fixture to initialize an in-memory test database
    @pytest.fixture(autouse=True)
    def setup_db(self):
        db = Database(db_name=":memory:")
        db.create_tables()
        return db

    def test_create_tables(self, setup_db):
        # Ensure that both 'habits' and 'tracking' tables are created.
        cursor = setup_db.conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        assert ('habits',) in tables
        assert ('tracking',) in tables

    def test_check_habit_exists(self, setup_db):
        # Verify that a habit can be correctly detected in the database.
        habit = Habit("Don't dream of non-existing habits", "Not even at night", "weekly")

        # Add the habit to the database.
        setup_db.add_habit_to_table(habit) # add habit

        # Check if the habit exists and verify results (True exits, False does not exist).
        assert setup_db.check_habit_exists("Don't dream of non-existing habits") is True
        assert setup_db.check_habit_exists("I am fictional") is False

    def test_add_habit_to_table(self, setup_db):
        # Validate that a habit can be successfully added to the database.
        habit = Habit("Test your code", "Do it thoroughly", "daily")
        habit_id = setup_db.add_habit_to_table(habit)

        # Fetch the added habit and verify stored values.
        cursor = setup_db.conn.execute("SELECT name, description, periodicity, "
                                       "creation_date FROM habits WHERE id = ?",
                                      (habit_id,))
        row = cursor.fetchone()
        assert row[0] == habit.get_name()
        assert row[1] == habit.get_description()
        assert row[2] == habit.get_periodicity()
        assert row[3] == habit.get_creation_date().strftime("%Y-%m-%d %H:%M:%S")

    def test_delete_habit_from_table(self, setup_db):
        # Test that a habit can be removed from the database.
        habit = Habit("Delete regularly", "Don't be sad about it", "daily")

        # Add and then delete the habit
        habit_id = setup_db.add_habit_to_table(habit)
        setup_db.delete_habit_from_table(habit_id)

        # Ensure the habit is deleted
        cursor = setup_db.conn.execute("SELECT * FROM habits WHERE id = ?", (habit_id,))
        assert cursor.fetchone() is None

    def test_add_streak_to_table(self, setup_db):
        # Check that a checkoff date is added for a habit
        habit = Habit("Don't get tired of testing", "Do it again", "weekly")
        habit_id = setup_db.add_habit_to_table(habit) # add habit

        # Add a checkoff date
        checkoff_date = datetime(2024, 10, 5) # define parameters
        setup_db.add_streak_to_table(habit_id, checkoff_date)

        # Verify the checkoff date was stored
        cursor = setup_db.conn.execute("SELECT checkoff_date FROM tracking WHERE habit_id = ?", (habit_id,))
        result = cursor.fetchone()

        assert result is not None, "No checkoff date found"
        assert result[0] == checkoff_date.strftime("%Y-%m-%d %H:%M:%S"), "Checkoff date does not match"

    def test_update_habit_in_table(self, setup_db):
        # Ensure that a habit can be updated in the database.
        habit = Habit("This is a not updated name", "This is the original description",
                      "daily")
        habit_id = setup_db.add_habit_to_table(habit)

        # Update the habit's name and description.
        new_name = "This is an updated name"
        new_description = "This is the updated description"
        setup_db.update_habit_in_table(habit_id, new_name, new_description)

        # Fetch and verify the updated habit
        cursor = setup_db.conn.execute("SELECT name, description FROM habits WHERE id = ?", (habit_id,))
        updated_habit = cursor.fetchone()

        assert updated_habit is not None, "Habit not found"
        assert updated_habit[0] == new_name, "Habit name was not updated"
        assert updated_habit[1] == new_description, "Habit description was not updated"

    def test_get_all_habits(self, setup_db):
        # Test retrieval of all habits from the database.
        habit_1 = Habit("Do yoga", "Connect to your inner self", "weekly")
        habit_2 = Habit("Go for a walk", "Get some air", "daily")

        # Add habits to the database
        setup_db.add_habit_to_table(habit_1)
        setup_db.add_habit_to_table(habit_2)

        # Fetch all habits and verify the list
        habits = setup_db.get_all_habits()
        assert len(habits) == 2
        assert habits[0]['name'] == habit_1.get_name()
        assert habits[1]['name'] == habit_2.get_name()

    def test_get_all_checkoff_dates(self, setup_db):
        # Ensure that all checkoff dates for a habit can be retrieved.
        habit = Habit("Get your checkoff_dates", "all of them", "weekly")
        habit_id = setup_db.add_habit_to_table(habit)

        # Add multiple checkoff dates
        checkoff_dates = [
            datetime(2024, 10, 3),
            datetime(2024, 10, 4, 14, 30), # try with hours and minutes
            datetime(2024, 10, 7, 8, 45, 30) # try also with seconds
        ]
        for date in checkoff_dates:
            setup_db.add_streak_to_table(habit_id, date)

        # Fetch and verify the checkoff dates
        fetched_dates = setup_db.get_all_checkoff_dates(habit_id)
        assert len(fetched_dates) == len(checkoff_dates), "This numbers do not match."
        for i in range(len(checkoff_dates)):
            assert fetched_dates[i] == checkoff_dates[i], f"Checkoff date at index {i} does not match."

    def test_get_habit_id(self, setup_db):
        # Test that a habit's ID can be retrieved by name.
        habit = Habit("Get your habit by ID", "This should work", "daily")
        habit_id = setup_db.add_habit_to_table(habit)

        # Fetch and verify the habit's ID
        fetched_id = setup_db.get_habit_id("Get your habit by ID")
        assert fetched_id == habit_id, "The fetched habit ID does not match the inserted habit ID."