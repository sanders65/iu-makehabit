from datetime import datetime

import pytest
from analyse import Analyse
from habit import Habit
from db import Database


# Set up a class for analyse-related tests
class TestAnalyse:

    # Use a fixture to initialize an in-memory test database.
    @pytest.fixture(autouse=True)
    def setup_analyse(self):
        db = Database(db_name=":memory:")
        db.create_tables()
        analyse = Analyse(db_name=":memory:")
        return analyse

    def test_get_all_stored_habits(self, setup_analyse):
        # Test that all habits with and without checkoff dates can be analyzed
        db = setup_analyse.db
        habit_1 = Habit("Do yoga", "Connect to your inner self", "weekly")
        habit_2 = Habit("Go for a walk", "Get some air", "daily")

        db.add_habit_to_table(habit_1)  # add habit
        db.add_habit_to_table(habit_2)  # add habit

        # check and verify
        all_habits = setup_analyse.get_all_stored_habits()

        assert "Do yoga" in all_habits
        assert "Go for a walk" in all_habits

    def test_get_all_checked_off_habits(self, setup_analyse):
        # Test that all habits with at least one checkoff date can be analyzed
        db = setup_analyse.db
        habit_1 = Habit("Do yoga", "Connect to your inner self", "weekly")
        habit_2 = Habit("Go for a walk", "Get some air", "daily")
        habit_3 = Habit("Do exercises", "Strengthen your body", "daily")

        habit_id1 = db.add_habit_to_table(habit_1) # add habit
        habit_id2 = db.add_habit_to_table(habit_2) # add habit
        habit_id3 = db.add_habit_to_table(habit_3)  # add habit

        db.add_streak_to_table(habit_id1, habit_1.get_creation_date()) # add checkoff dates
        db.add_streak_to_table(habit_id2, habit_2.get_creation_date())  # add checkoff dates
        # Don't add checkoff date for habit_3

        # check and verify
        tracked_habits = setup_analyse.get_all_checked_off_habits()

        assert "Do yoga" in tracked_habits
        assert "Go for a walk" in tracked_habits
        assert "Do exercise" not in tracked_habits

    def test_get_habits_by_periodicity(self, setup_analyse):
        # Test that habits can be filtered by periodicity
        db = setup_analyse.db
        habit_1 = Habit("Do yoga", "Connect to your inner self", "weekly")
        habit_2 = Habit("Go for a walk", "Get some air", "daily")
        habit_3 = Habit("Do exercises", "Strengthen your body", "daily")
        habit_4 = Habit("Visit a friend", "Care for your social skills", "weekly")

        db.add_habit_to_table(habit_1) # add habit
        habit_id2 = db.add_habit_to_table(habit_2) # add habit
        db.add_habit_to_table(habit_3) # add habit
        habit_id4 = db.add_habit_to_table(habit_4) # add habit

        db.add_streak_to_table(habit_id2, datetime(2024, 10, 5)) # add checkoff date
        db.add_streak_to_table(habit_id4, datetime(2024, 10, 1))  # add checkoff date

        # check and verify daily habits
        daily_habits_with_checkoff, daily_habits_without_checkoff = setup_analyse.get_habits_by_periodicity("daily")
        assert "Do yoga" not in daily_habits_with_checkoff and "Do yoga" not in daily_habits_without_checkoff #not daily
        assert "Go for a walk" in daily_habits_with_checkoff # daily and checked off
        assert "Do exercises" in daily_habits_without_checkoff # daily and not checked off
        assert ("Visit a friend" not in daily_habits_with_checkoff and
                "Visit a friend" not in daily_habits_without_checkoff) # not daily

        # check and verify weekly habits
        weekly_habits_with_checkoff, weekly_habits_without_checkoff = setup_analyse.get_habits_by_periodicity("weekly")
        assert "Do yoga" in weekly_habits_without_checkoff # weekly and not checked off
        assert ("Go for a walk" not in weekly_habits_with_checkoff and
                "Go for a walk" not in weekly_habits_without_checkoff) # not weekly
        assert ("Do exercises" not in weekly_habits_with_checkoff and
                "Do exercises" not in weekly_habits_without_checkoff) # not weekly
        assert "Visit a friend" in weekly_habits_with_checkoff # weekly and checked off

    def test_get_longest_streak_daily(self, setup_analyse):
        # Test that the daily habit with the longest streak is shown
        db = setup_analyse.db
        habit_1 = Habit("Do exercises", "Strengthen your body", "daily")
        habit_2 = Habit("Go for a walk", "Get some air", "daily")
        habit_3 = Habit("Read the newspaper", "Inform yourself", "daily")

        habit_id1 = db.add_habit_to_table(habit_1) # add habit
        habit_id2 = db.add_habit_to_table(habit_2) # add habit
        habit_id3 = db.add_habit_to_table(habit_3)  # add habit

        # Add the same checkoff dates to habit_1 and habit_3 so they have the same streak
        for i in range(3):
            db.add_streak_to_table(habit_id1, datetime(2024, 10, 1 + i))
            db.add_streak_to_table(habit_id3, datetime(2024, 10, 1 + i))
        # Add just one checkoff date to habit_2
        db.add_streak_to_table(habit_id2, datetime(2024, 10, 2))

        # check and verify
        habit_name, longest_streak = setup_analyse.get_longest_streak_daily()
        assert set(habit_name) == {"Do exercises", "Read the newspaper"}
        assert longest_streak == 3

    def test_get_longest_streak_weekly(self, setup_analyse):
        # Test that the weekly habit with the longest streak is shown
        db = setup_analyse.db
        habit_1 = Habit("Do yoga", "Connect to your inner self", "weekly")
        habit_2 = Habit("Visit a friend", "Care for your social skills", "weekly")
        habit_3 = Habit("Water the plants", "They will look nicer", "weekly")

        habit_id1 = db.add_habit_to_table(habit_1) # add habit
        habit_id2 = db.add_habit_to_table(habit_2) # add habit
        habit_id3 = db.add_habit_to_table(habit_3)  # add habit

        # Add the same checkoff dates to habit_1 and habit_3 so they have the same streak
        db.add_streak_to_table(habit_id1, datetime(2024, 10, 1)) # week 1 for habit_1
        db.add_streak_to_table(habit_id1, datetime(2024, 10, 8)) # week 2 for habit_1
        db.add_streak_to_table(habit_id3, datetime(2024, 10, 1))  # week 1 for habit_3
        db.add_streak_to_table(habit_id3, datetime(2024, 10, 8))  # week 2 for habit_3

        # Add just one checkoff date to habit_2
        db.add_streak_to_table(habit_id2, datetime(2024, 10, 2))  # week 1 for habit_2

        # Check and verify
        habit_name, longest_streak = setup_analyse.get_longest_streak_weekly()
        assert set(habit_name) == {"Do yoga", "Water the plants"}
        assert longest_streak == 2

    def test_get_longest_streak_by_name(self, setup_analyse):
        db = setup_analyse.db
        habit = Habit("Test your code", "Do it thoroughly", "daily")

        habit_id = db.add_habit_to_table(habit) # add habit
        # add multiple checkoff dates
        for i in range(5):
            db.add_streak_to_table(habit_id, datetime(2024, 10, 1 + i))

        # Check and verify
        habit_name, streak = setup_analyse.get_longest_streak_by_name("Test your code")
        assert habit_name == "Test your code"
        assert streak == 5