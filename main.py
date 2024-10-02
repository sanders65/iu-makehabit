import questionary
from db import get_db
from habit import Habit, Streak
from analyse import calculate_streak, list_all_habits
from datetime import date

def main_menu():
    db = get_db()

    questionary.confirm("Welcome! Are you ready to start?").ask()

    stop = False
    while not stop:
        choice = questionary.select(
            "What do you want to do?",
            choices = ["Add habit", "Check off habit", "Analyse habits", "Delete habit", "Exit"]
        ).ask()

        if choice == "Add habit":
            name = questionary.text("What is the name of your habit?").ask()
            if not name:
                raise NameError
            periodicity = questionary.select("How often do you want to perform your new habit?",
                                             choices=["daily", "weekly"]).ask()
            habit = Habit(name, periodicity, creation_date = date.today(), streak = 0)
            habit.store_habit_data(db)
            print("Your new habit was saved successfully!")
            main_menu()

        elif choice == "Check off habit":
            name = questionary.text("What is the name of the habit you want to check off?").ask()
            if not name:
                raise NameError
            check_off = Streak(name, checkoff_date = date.today(), streak = 1)
            check_off.store_tracking_data(db)
            print("Your habit was checked off successfully!")

        elif choice == "Analyse habits":
            analyse_choices = questionary.select("What do you want to analyze?",
                choices=["Get a list of all habits",
                    "Get a list of all habits with the same periodicity",
                    "Show my longest streak of all daily habits",
                    "Show my longest streak of all weekly habits",
                    "Show my longest streak for a specific habit",
                    "Exit"]).ask()

            if analyse_choices == "Get a list of all habits":
                print("This is the list of all your habits:")
                return list_all_habits(db)

            elif analyse_choices == "Get a list of all habits with the same periodicity":
                questionary.select("Which periodicity do you want to analyse?",
                                   choices=["daily", "weekly"]).ask()


            elif analyse_choices == "Show my longest streak of all daily habits":
                pass

            elif analyse_choices == "Show my longest streak of a specific habit":
                pass

            elif analyse_choices == "Show my longest streak of all daily habits":
                pass

            else:
                main_menu()

        elif choice == "Delete habit":
            name = questionary.text("What is the name of the habit you want to delete?").ask()
            if not name:
                raise NameError
            questionary.confirm("Are you really sure you want to delete that habit?").ask()
            db.remove_habit_data(name)
            print("Your habit was deleted successfully!")
            main_menu()

        elif choice == "Exit":
            print("See you again soon!")
            stop = True

if __name__ == "__main__":
    main_menu()
