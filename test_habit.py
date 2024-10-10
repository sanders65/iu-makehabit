import pytest
from datetime import datetime, timedelta
from habit import Habit


# Use a fixture to create a list of habit instances to use in tests.
@pytest.fixture
def sample_habits():
    habit_1 = Habit("Do yoga", "Connect to your inner self", "weekly")
    habit_2 = Habit("Go for a walk", "Get some air", "daily")
    habit_3 = Habit("Do exercises", "Strengthen your body", "daily")
    habit_4 = Habit("Visit a friend", "Care for your social skills", "weekly")
    habit_5 = Habit("Search jobs", "Get out of your comfort zone", "daily")
    return [habit_1, habit_2, habit_3, habit_4, habit_5]

# Use a fixture to simulate checkoff history for habits with different patterns.
@pytest.fixture
def sample_checkoff_dates(sample_habits):
    base_date = datetime(2024, 10, 1)

    # Set habit_1 (weekly) to get checked off on every week for a month
    for i in range(4):
        sample_habits[0].checkoff_habit(base_date - timedelta(weeks=i))

    # Set habit_2 (daily) to get checked off daily for 13 times
    for i in range(13):
        sample_habits[1].checkoff_habit(base_date - timedelta(days=i))

    # Set habit_3 (daily) to get checked off three times in a row and then again on day 5 and 6, i.e. it breaks
    for i in range(3):
        sample_habits[2].checkoff_habit(base_date - timedelta(days=i + 1))
    sample_habits[2].checkoff_habit(base_date - timedelta(days=5))
    sample_habits[2].checkoff_habit(base_date - timedelta(days=6))

    # Set habit_4 (weekly) to get checked off two times and then again on week 4, i.e. it breaks
    for i in range(2):
        sample_habits[3].checkoff_habit(base_date - timedelta(weeks=i))
    sample_habits[3].checkoff_habit(base_date - timedelta(weeks=4))

    # Set habit_5 (daily) to get checked off four times
    for i in range(4):
        sample_habits[4].checkoff_habit(base_date - timedelta(days=i))

# Test that a habit can get created.
def test_habit_creation():
    habit = Habit("Test habit", "Test description", "daily")
    assert habit.get_name() == "Test habit"
    assert habit.get_description() == "Test description"
    assert habit.get_periodicity() == "daily"

# Test if a habit can get edited.
def test_edit_habit(sample_habits):
    habit = sample_habits[0]
    habit.edit_habit("Do MORE exercises", "Strengthen your body MORE")
    assert habit.get_name() == "Do MORE exercises"
    assert habit.get_description() == "Strengthen your body MORE"

# Test if a daily habit raises its streak when gets checked off and also breaks if not gets checked off.
def test_streak_daily(sample_habits):
    habit = sample_habits[1]
    base_date = datetime(2024, 10, 1)
    habit.checkoff_habit(base_date + timedelta(days=1))
    assert habit.streak() == 1

    habit.checkoff_habit(base_date + timedelta(days=2))
    assert habit.streak() == 2

    habit.checkoff_habit(base_date + timedelta(days=4))
    assert habit.streak() == 1 # Streak broke and begins again at 1

# Test if a weekly habit raises its streak when gets checked off and also breaks if not gets checked off.
def test_streak_weekly(sample_habits):
    habit = sample_habits[3]
    base_week = datetime(2024, 10, 1) - timedelta(days=datetime(2024, 10, 1).weekday())
    habit.checkoff_habit(base_week + timedelta(weeks=1))
    assert habit.streak() == 1

    habit.checkoff_habit(base_week + timedelta(weeks=2))
    habit.checkoff_habit(base_week + timedelta(weeks=3))
    assert habit.streak() == 3

    habit.checkoff_habit(base_week + timedelta(weeks=5))
    assert habit.streak() == 1 # Streak broke and begins again at 1