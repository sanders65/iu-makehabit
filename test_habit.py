import pytest
from datetime import datetime, timedelta
from habit import Habit


# Fixture that creates a list of sample Habit instances to used in various tests.
@pytest.fixture
def sample_habits():
    habit_1 = Habit("Do yoga", "Connect to your inner self", "weekly")
    habit_2 = Habit("Go for a walk", "Get some air", "daily")
    habit_3 = Habit("Do exercises", "Strengthen your body", "daily")
    habit_4 = Habit("Visit a friend", "Care for your social skills", "weekly")
    habit_5 = Habit("Search jobs", "Get out of your comfort zone", "daily")
    return [habit_1, habit_2, habit_3, habit_4, habit_5]

# Fixture that simulates checkoff dates for the sample habits to reflect different patterns.
@pytest.fixture
def sample_checkoff_dates(sample_habits):
    base_date = datetime(2024, 10, 1)

    # Check off habit_1 (weekly) once per week for four weeks
    for i in range(4):
        sample_habits[0].checkoff_habit(base_date - timedelta(weeks=i))

    # Check off habit_2 (daily) for 13 consecutive days
    for i in range(13):
        sample_habits[1].checkoff_habit(base_date - timedelta(days=i))

    # Check off habit_3 (daily) for three consecutive days, then skip and check off on day 5 and 6, i.e. it breaks
    for i in range(3):
        sample_habits[2].checkoff_habit(base_date - timedelta(days=i + 1))
    sample_habits[2].checkoff_habit(base_date - timedelta(days=5))
    sample_habits[2].checkoff_habit(base_date - timedelta(days=6))

    # Check off habit_4 (weekly) for two consecutive weeks, then again in week 4, i.e. it breaks
    for i in range(2):
        sample_habits[3].checkoff_habit(base_date - timedelta(weeks=i))
    sample_habits[3].checkoff_habit(base_date - timedelta(weeks=4))

    # Check off habit_5 (daily) for four consecutive days
    for i in range(4):
        sample_habits[4].checkoff_habit(base_date - timedelta(days=i))

# Test that verifies the creation of a habit with proper attributes.
def test_habit_creation():
    habit = Habit("Test habit", "Test description", "daily")
    assert habit.get_name() == "Test habit"
    assert habit.get_description() == "Test description"
    assert habit.get_periodicity() == "daily"

# Test that verifies the editing functionality of a habit, ensuring the name and description can be updated.
def test_edit_habit(sample_habits):
    habit = sample_habits[0]
    habit.edit_habit("Do MORE exercises", "Strengthen your body MORE")
    assert habit.get_name() == "Do MORE exercises"
    assert habit.get_description() == "Strengthen your body MORE"

# Test that checks whether a daily habit's streak increases with consecutive checkoffs and resets after a missed day.
def test_streak_daily(sample_habits):
    habit = sample_habits[1]
    base_date = datetime(2024, 10, 1)
    habit.checkoff_habit(base_date + timedelta(days=1))
    assert habit.streak() == 1

    habit.checkoff_habit(base_date + timedelta(days=2))
    assert habit.streak() == 2

    habit.checkoff_habit(base_date + timedelta(days=4)) # Skip day 3
    assert habit.streak() == 1 # Streak breaks due to missed checkoff

# Test that checks whether a weekly habit's streak increases with consecutive checkoffs and resets after a missed week.
def test_streak_weekly(sample_habits):
    habit = sample_habits[3]
    base_week = (
            datetime(2024, 10, 1) - timedelta(days=datetime(2024, 10, 1).weekday()))
    habit.checkoff_habit(base_week + timedelta(weeks=1))
    assert habit.streak() == 1

    habit.checkoff_habit(base_week + timedelta(weeks=2))
    habit.checkoff_habit(base_week + timedelta(weeks=3))
    assert habit.streak() == 3

    habit.checkoff_habit(base_week + timedelta(weeks=5)) # Skip week 4
    assert habit.streak() == 1 # Streak breaks due to missed checkoff