from db import get_habit_data, get_all_habit_data


def calculate_streak(db, name):
    data = get_habit_data(db, name)
    return len(data)

def list_all_habits(db):
    data = get_all_habit_data(db)
    return data




