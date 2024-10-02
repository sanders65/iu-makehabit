from habit import Habit, Streak
from db import get_db, add_habit_data, add_tracking_data, get_habit_data, remove_habit_data
from analyse import calculate_streak

class TestHabit:

    def setup_method(self):
        self.db = get_db('test.db')
        add_habit_data(self.db, "do exercise", "daily", "2024-09-28", 0)
        add_tracking_data(self.db, "do exercise", "2024-09-29", 1)
        add_tracking_data(self.db, "do exercise", "2024-09-30", 2)
        add_tracking_data(self.db, "do exercise", "2024-10-01", 3)


    def test_habit(self):
        habit = Habit("go for a walk", "daily")
        streak = Streak("go for a walk", "2024-10-01", 1)
        habit.store_habit_data(self.db)
        streak.store_tracking_data(self.db)

        streak.streak_raise()
        streak.streak_break()
        streak.streak_raise()

    def test_streak(self):
        data = get_habit_data(self.db, "do exercise")
        assert len(data) == 3

        streak = calculate_streak(self.db, "do exercise")
        assert streak == 3

    def test_remove_habit_data(self):
        db = get_db('test.db')
        delete = remove_habit_data(db,"go for a walk", "daily", "2024-10-01", 0)
        assert delete is True

    def teardown_method(self):
        import os
        os.remove('test.db')

