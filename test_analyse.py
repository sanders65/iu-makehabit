from datetime import datetime
import pytest
from analyse import Analyse
from habit import Habit
from db import Database


# Test for Analyse class functions
class TestAnalyse:

    # Fixture to set up an in-memory test database and the Analyse class.
    @pytest.fixture(autouse=True)
    def setup_analyse(self):
        db = Database(db_name=":memory:")
        db.create_tables()
        analyse = Analyse(db)
        return db, analyse

    def test_get_all_stored_habits(self, setup_analyse):
        # Test that all habits (with and without checkoff dates) can be retrieved.
        db, analyse = setup_analyse
        habit_1 = Habit("Do yoga", "Connect to your inner self", "weekly")
        habit_2 = Habit("Go for a walk", "Get some air", "daily")

        db.add_habit_to_table(habit_1)
        db.add_habit_to_table(habit_2)

        # Verify that all habits are retrieved.
        all_habits = analyse.get_all_stored_habits()

        assert "Do yoga" in all_habits
        assert "Go for a walk" in all_habits

    def test_get_all_checked_off_habits(self, setup_analyse):
        # Test that only habits with at least one checkoff date are retrieved.
        db, analyse = setup_analyse
        habit_1 = Habit("Do yoga", "Connect to your inner self", "weekly")
        habit_2 = Habit("Go for a walk", "Get some air", "daily")
        habit_3 = Habit("Do exercises", "Strengthen your body", "daily")

        habit_id1 = db.add_habit_to_table(habit_1)
        habit_id2 = db.add_habit_to_table(habit_2)
        habit_id3 = db.add_habit_to_table(habit_3)

        db.add_streak_to_table(habit_id1, habit_1.get_creation_date())
        db.add_streak_to_table(habit_id2, habit_2.get_creation_date())
        # Don't add checkoff date for habit_3

        # Verify that only checked-off habits are returned.
        tracked_habits = analyse.get_all_checked_off_habits()

        assert "Do yoga" in tracked_habits
        assert "Go for a walk" in tracked_habits
        assert "Do exercise" not in tracked_habits

    def test_get_habits_by_periodicity(self, setup_analyse):
        # Test that habits can be filtered by periodicity (daily/weekly).
        db, analyse = setup_analyse
        habit_1 = Habit("Do yoga", "Connect to your inner self", "weekly")
        habit_2 = Habit("Go for a walk", "Get some air", "daily")
        habit_3 = Habit("Do exercises", "Strengthen your body", "daily")
        habit_4 = Habit("Visit a friend", "Care for your social skills", "weekly")

        db.add_habit_to_table(habit_1)
        habit_id2 = db.add_habit_to_table(habit_2)
        db.add_habit_to_table(habit_3)
        habit_id4 = db.add_habit_to_table(habit_4)

        db.add_streak_to_table(habit_id2, datetime(2024, 10, 5)) # Checkoff habit_2
        db.add_streak_to_table(habit_id4, datetime(2024, 10, 1))  # Checkoff habit_4

        # Verify filtering for daily habits.
        daily_habits_with_checkoff, daily_habits_without_checkoff = analyse.get_habits_by_periodicity("daily")
        assert "Go for a walk" in daily_habits_with_checkoff # Checked-off daily habit
        assert "Do exercises" in daily_habits_without_checkoff # Not checked-off daily habit
        assert ("Do yoga" not in daily_habits_with_checkoff and
                "Do yoga" not in daily_habits_without_checkoff) # Not a daily habit
        assert ("Visit a friend" not in daily_habits_with_checkoff and
                "Visit a friend" not in daily_habits_without_checkoff) # Not a daily habit

        # Verify filtering for weekly habits.
        weekly_habits_with_checkoff, weekly_habits_without_checkoff = analyse.get_habits_by_periodicity("weekly")
        assert "Do yoga" in weekly_habits_without_checkoff # Not checked-off weekly habit
        assert "Visit a friend" in weekly_habits_with_checkoff # Checked-off weekly habit
        assert ("Go for a walk" not in weekly_habits_with_checkoff and
                "Go for a walk" not in weekly_habits_without_checkoff) # Not a weekly habit
        assert ("Do exercises" not in weekly_habits_with_checkoff and
                "Do exercises" not in weekly_habits_without_checkoff) # Not a weekly habit

    def test_get_longest_streak_daily(self, setup_analyse):
        # Test that the daily habit with the longest streak is identified correctly.
        db, analyse = setup_analyse
        habit_1 = Habit("Do exercises", "Strengthen your body", "daily")
        habit_2 = Habit("Go for a walk", "Get some air", "daily")
        habit_3 = Habit("Read the newspaper", "Inform yourself", "daily")

        habit_id1 = db.add_habit_to_table(habit_1)
        habit_id2 = db.add_habit_to_table(habit_2)
        habit_id3 = db.add_habit_to_table(habit_3)

        # Add consecutive checkoff dates to habit_1 and habit_3 to create equal streaks.
        for i in range(3):
            db.add_streak_to_table(habit_id1, datetime(2024, 10, 1 + i))
            db.add_streak_to_table(habit_id3, datetime(2024, 10, 1 + i))
        # Add just one checkoff date to habit_2.
        db.add_streak_to_table(habit_id2, datetime(2024, 10, 2))

        # Verify that both habits with the longest streak are identified.
        habit_name, longest_streak = analyse.get_longest_streak_daily()
        assert set(habit_name) == {"Do exercises", "Read the newspaper"}
        assert longest_streak == 3

    def test_get_longest_streak_weekly(self, setup_analyse):
        # Test that the weekly habit with the longest streak is identified correctly.
        db, analyse = setup_analyse
        habit_1 = Habit("Do yoga", "Connect to your inner self", "weekly")
        habit_2 = Habit("Visit a friend", "Care for your social skills", "weekly")
        habit_3 = Habit("Water the plants", "They will look nicer", "weekly")

        habit_id1 = db.add_habit_to_table(habit_1)
        habit_id2 = db.add_habit_to_table(habit_2)
        habit_id3 = db.add_habit_to_table(habit_3)

        # Add consecutive weekly checkoff dates for habit_1 and habit_3.
        db.add_streak_to_table(habit_id1, datetime(2024, 10, 1)) # Week 1 for habit_1
        db.add_streak_to_table(habit_id1, datetime(2024, 10, 8)) # Week 2 for habit_1
        db.add_streak_to_table(habit_id3, datetime(2024, 10, 1)) # Week 1 for habit_3
        db.add_streak_to_table(habit_id3, datetime(2024, 10, 8)) # Week 2 for habit_3
        # Add just one checkoff date to habit_2
        db.add_streak_to_table(habit_id2, datetime(2024, 10, 2))  # Week 1 for habit_2

        # Verify that both habits with the longest streak are identified.
        habit_name, longest_streak = analyse.get_longest_streak_weekly()
        assert set(habit_name) == {"Do yoga", "Water the plants"}
        assert longest_streak == 2

    def test_get_longest_streak_by_name(self, setup_analyse):
        # Test that the longest streak for a specific habit is calculated correctly.
        db, analyse = setup_analyse
        habit = Habit("Test your code", "Do it thoroughly", "daily")

        habit_id = db.add_habit_to_table(habit)

        # Add multiple consecutive checkoff dates.
        for i in range(5):
            db.add_streak_to_table(habit_id, datetime(2024, 10, 1 + i))

        # Verify that the longest streak for the specific habit is correct.
        habit_name, streak = analyse.get_longest_streak_by_name("Test your code")
        assert habit_name == "Test your code"
        assert streak == 5