import pytest
from habit import Habit
from db import Database
from datetime import datetime


# Set up a class for database-related tests
class TestDatabase:

    # Use a fixture to initialize an in-memory test database.
    @pytest.fixture(autouse=True)
    def setup_db(self):
        db = Database(db_name=":memory:")
        db.create_tables()
        return db

    def test_create_tables(self, setup_db):
        # Test that tables are established as wanted.
        cursor = setup_db.conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        assert ('habits',) in tables
        assert ('tracking',) in tables

    def test_check_habit_exists(self, setup_db):
        # Test if a habit exists in the database
        habit = Habit("Don't dream of non-existing habits", "Not even at night", "weekly")

        setup_db.add_habit_to_table(habit) # add habit

        #check and verify (True exits, False does not exist)
        assert setup_db.check_habit_exists("Don't dream of non-existing habits") is True
        assert setup_db.check_habit_exists("I am fictional") is False

    def test_add_habit_to_table(self, setup_db):
        # Test that a habit gets added to the database.
        habit = Habit("Test your code", "Do it thoroughly", "daily")
        habit_id = setup_db.add_habit_to_table(habit)

        cursor = setup_db.conn.execute("SELECT name, description, periodicity, creation_date FROM habits WHERE id = ?",
                                      (habit_id,))
        row = cursor.fetchone()
        assert row[0] == habit.get_name()
        assert row[1] == habit.get_description()
        assert row[2] == habit.get_periodicity()
        assert row[3] == habit.get_creation_date().strftime("%Y-%m-%d %H:%M:%S")

    def test_delete_habit_from_table(self, setup_db):
        # Test to delete a habit from the database.
        habit = Habit("Delete regularly", "Don't be sad about it", "daily")

        habit_id = setup_db.add_habit_to_table(habit) # add habit

        setup_db.delete_habit_from_table(habit_id) # delete habit

        # check and verify
        cursor = setup_db.conn.execute("SELECT * FROM habits WHERE id = ?", (habit_id,))
        assert cursor.fetchone() is None

    def test_add_streak_to_table(self, setup_db):
        # Test that a checkoff date gets added to the database
        habit = Habit("Don't get tired of testing", "Do it again", "weekly")
        habit_id = setup_db.add_habit_to_table(habit) # add habit

        checkoff_date = datetime(2024, 10, 5) # define parameters
        setup_db.add_streak_to_table(habit_id, checkoff_date)

        # check and verify
        cursor = setup_db.conn.execute("SELECT checkoff_date FROM tracking WHERE habit_id = ?", (habit_id,))
        result = cursor.fetchone()

        assert result is not None, "No checkoff date found"
        assert result[0] == checkoff_date.strftime("%Y-%m-%d %H:%M:%S"), "Checkoff date does not match"

    def test_update_habit_in_table(self, setup_db):
        # Test that a habit can get updated and stored in the database
        habit = Habit("This is a not updated name", "This is the original description", "daily")
        habit_id = setup_db.add_habit_to_table(habit)

        # Define the updated parameters
        new_name = "This is an updated name"
        new_description = "This is the updated description"
        setup_db.update_habit_in_table(habit_id, new_name, new_description)

        # check and verify
        cursor = setup_db.conn.execute("SELECT name, description FROM habits WHERE id = ?", (habit_id,))
        updated_habit = cursor.fetchone()

        assert updated_habit is not None, "Habit not found"
        assert updated_habit[0] == new_name, "Habit name was not updated"
        assert updated_habit[1] == new_description, "Habit description was not updated"

    def test_get_all_habits(self, setup_db):
        # Test to get all habits from the database
        habit_1 = Habit("Do yoga", "Connect to your inner self", "weekly")
        habit_2 = Habit("Go for a walk", "Get some air", "daily")

        setup_db.add_habit_to_table(habit_1) # add habit
        setup_db.add_habit_to_table(habit_2) # add habit

        habits = setup_db.get_all_habits() # get all habits

        # check and verify
        assert len(habits) == 2
        assert habits[0]['name'] == habit_1.get_name()
        assert habits[1]['name'] == habit_2.get_name()

    def test_get_all_checkoff_dates(self, setup_db):
        # Test that all checkoff dates from one habit can be retrieved
        habit = Habit("Get your checkoff_dates", "all of them", "weekly")
        habit_id = setup_db.add_habit_to_table(habit) # add habit

        # set some checkoff dates
        checkoff_dates = [
            datetime(2024, 10, 3),
            datetime(2024, 10, 4),
            datetime(2024, 10, 7)
        ]
        for date in checkoff_dates:
            setup_db.add_streak_to_table(habit_id, date)

        fetched_dates = setup_db.get_all_checkoff_dates(habit_id)

        # check and verify
        assert len(fetched_dates) == len(checkoff_dates), "This numbers do not match."
        for i in range(len(checkoff_dates)):
            assert fetched_dates[i] == checkoff_dates[i], f"Checkoff date at index {i} does not match."

    def test_get_habit_id(self, setup_db):
        habit = Habit("Get your habit by ID", "This should work", "daily")
        habit_id = setup_db.add_habit_to_table(habit) #add habit

        # check and verify
        fetched_id = setup_db.get_habit_id("Get your habit by ID")

        assert fetched_id == habit_id, "The fetched habit ID does not match the inserted habit ID."



