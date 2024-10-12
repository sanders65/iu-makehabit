from datetime import datetime
import questionary
import sqlite3
import os
from db import Database
from habit import Habit
from analyse import Analyse

current_db = "main.db" # Default database, make variable global for the current db

# Function to initialize the Database and Analyse instances
def initialize_modules():
    global db, analyse
    db = Database(db_name=current_db) # Pass current_db to Database instance
    analyse = Analyse(db) # Pass the db instance to Analyse

def load_sql_script(script_path):
    """Load SQL script into the specified database."""
    global current_db, db
    try:
        current_db = "example.db" # Set current_db to example.db

        with sqlite3.connect(current_db) as conn:
            with open(script_path, 'r') as sql_file:
                sql_script = sql_file.read()
            conn.executescript(sql_script)

        print(f"Example data was successfully loaded into {current_db}. "
              "'Make it a Habit' now uses the predefined example data.")

        db = Database(db_name=current_db) # Reinitialize modules to use example.db

    except Exception as e:
        print(f"Error loading SQL script: {e}")

def prompt_load_example_data():
    """Ask the user, if they want to load example data or not."""
    load_example = questionary.confirm("Do you want to load the example data "
                                       "with predefined habits and checkoff dates?").ask()
    if load_example:
        if os.path.exists("example_habit.sql"):
            load_sql_script("example_habit.sql")
        else:
            print("The file 'example_habit.sql' could not be found. "
                  "Please make sure that the file is in the project directory.")
    else:
        print("Okay, we are continuing without loading the example data.")

def main_menu():
    # Start with a welcome message
    start = questionary.confirm("Welcome! Are you ready to start?").ask()

    if not start:
        exit_cli() # Exit the program if user don't want to start

    choice = questionary.select(
        "What do you want to do?",
        choices = ["Add habit", "Check off habit", "Edit habit", "Analyse habits", "Delete habit", "Exit"]
    ).ask()

    # Split choices into separated functions to keep better track
    if choice == "Add habit":
        add_habit_cli()
    elif choice == "Check off habit":
        checkoff_habit_cli()
    elif choice == "Edit habit":
        edit_habit_cli()
    elif choice == "Analyse habits":
        analyse_habit_cli()
    elif choice == "Delete habit":
        delete_habit_cli()
    elif choice == "Exit":
        exit_cli()

def add_habit_cli():
    # Define how habits are added by the user
    name = questionary.text("Please enter the name of your habit.").ask()

    # Check for already existing habit names to prevent duplicates
    existing_habits = [habit['name'] for habit in db.get_all_habits()]
    if name in existing_habits:
        print(f"The habit '{name}' already exists. Please enter another name for your new habit.")
        add_habit_cli() # Come back to start
        return

    description = questionary.text("If you want to, you can add a description.").ask()
    periodicity = questionary.select(
        "Please choose the frequency of your habit.", choices=["daily", "weekly"]
    ).ask()

    habit = Habit(name, description, periodicity)
    db.add_habit_to_table(habit)
    print(f"Your new habit '{name}' was added successfully!")
    main_menu()

def checkoff_habit_cli():
    # Define how habits are checked off by the user
    habits = db.get_all_habits()
    if not habits: # Check if there are habits, if not go back to main menu
        print("Sorry, there are no habits to check off.")
        main_menu()
        return

    habit_names = [habit['name'] for habit in habits]
    habit_name = questionary.select("Which habit do you want to check off?", choices=habit_names).ask()

    # Look for habit details
    habit_data = next(h for h in habits if h['name'] == habit_name)
    habit_id = db.get_habit_id(habit_name)

    # Look for checkoff dates in the database and create object
    checkoff_dates = db.get_all_checkoff_dates(habit_id)
    habit = Habit(habit_data['name'], habit_data['description'], habit_data['periodicity'])
    habit.checkoff_dates = checkoff_dates

    # Ask if user wants to add a custom date or today's date
    use_custom_date = questionary.confirm("Do you want to enter a custom checkoff date?").ask()

    if use_custom_date:
        while True:
            # Ask user to input a date
            custom_date_str = questionary.text("Please enter your custom checkoff date, use format YYYY-MM-DD:").ask()
            try:
                custom_date = datetime.strptime(custom_date_str, "%Y-%m-%d")
                break # Exit loop when input is valid
            except ValueError:
                print("You entered an invalid date format. Please try again.")

    else:
        # Use today's date as default
        custom_date = datetime.now()

    # Use checkoff logic from habit.py to ensure habit can just get checked off once
    if habit.checkoff_habit(checkoff_date=custom_date): # Here the user input or default value is passed
        db.add_streak_to_table(habit_id, custom_date)
        print(f"Your habit '{habit_name}' was checked off successfully on {custom_date}!")
    else:
        print(f"Your habit '{habit_name}' was already checked off in the given periodicity.")

    main_menu()

def edit_habit_cli():
    print(f" Currently used db: {current_db}")
    # Define how habits are edited by the user
    habits = db.get_all_habits()
    if not habits:
        print("Sorry, there are no habits to edit.")
        main_menu()
        return

    habit_names = [habit['name'] for habit in habits]
    habit_name = questionary.select("Which habit do you want to edit?", choices=habit_names).ask()

    # Start a loop to check for already existing habit names to prevent duplicates

    while True:
        new_name = questionary.text("Please enter the new name for your habit.").ask()

    # But make sure, that the same name can be reused
        existing_habits = [habit['name'] for habit in habits if habit['name'] != habit_name]
        if new_name in existing_habits:
            print(f"The habit '{new_name}' already exists. Please enter another name for your new habit.")
        else:
            break # Exit loop if valid name is found

    # If there are no duplicates, proceed with editing the habit
    new_description = questionary.text("Please enter the new description for your habit.").ask()
    habit_id = db.get_habit_id(habit_name)
    db.update_habit_in_table(habit_id, new_name, new_description)
    print(f"Your habit '{new_name}' was edited successfully!")
    main_menu()

def analyse_habit_cli():
    print(f" Currently used db: {current_db}")
    # Define how habits can get analyzed by the user
    choice = questionary.select(
        "What do you want to analyze?",
        choices=["Show all habits",
                 "Show all at least once checked off habits",
                 "Show all habits by periodicity",
                 "Show all at least once checked off habits by periodicity",
                 "Show longest streak for daily habits",
                 "Show longest streak for weekly habits",
                 "Show longest streak for a specific habit",
                 "Exit Analyse habits"]
        ).ask()

    if choice == "Show all habits":
        # Gets all stored habits (daily and weekly) with or without checkoff dates, sorted by id
        all_habits = analyse.get_all_stored_habits()
        if all_habits:
            print("These are all your currently tracked habits:", ", ".join(all_habits))
        else:
            print("There are no currently tracked habits.")
        main_menu()

    elif choice == "Show all at least once checked off habits":
        # Gets all stored habits (daily and weekly) with at least one checkoff dates, sorted by id
        tracked_habits = analyse.get_all_checked_off_habits()
        if tracked_habits:
            print("These are your currently tracked habits "
                  "with at least one checkoff date:", ", ".join(tracked_habits))
        else:
            print("There are no currently tracked habits.")
        main_menu()

    elif choice == "Show all habits by periodicity":
        periodicity = questionary.select("Please choose a periodicity to filter by.",
                                        choices=["daily", "weekly"]).ask()
        with_checkoff, without_checkoff = analyse.get_habits_by_periodicity(periodicity)

        # Gets all stored habits (daily OR weekly) with and without checkoff dates
        # Results are presented in two print statements, habits sorted by id
        print(f"Your {periodicity} habits with checkoff dates are:",
              ", ".join(with_checkoff) if with_checkoff else "None")
        print(f"Your {periodicity} habits without checkoff dates are:",
              ", ".join(without_checkoff) if without_checkoff else "None")
        main_menu()

    elif choice == "Show all at least once checked off habits by periodicity":
        periodicity = questionary.select("Please choose a periodicity to filter by.",
                                        choices=["daily", "weekly"]).ask()
        with_checkoff, _ = analyse.get_habits_by_periodicity(periodicity)

        # Gets all stored habits (daily OR weekly) with at least one checkoff date, sorted by id
        if with_checkoff:
            print(f"Your {periodicity} habits with at least one checkoff date are:",
                ", ".join(with_checkoff))
        else:
            print(f"There are not {periodicity} habits with at least one checkoff date.")
        main_menu()

    elif choice == "Show longest streak for daily habits":
        # Gets the daily habits with the longest streak
        habit_name, streak = analyse.get_longest_streak_daily()
        if habit_name:
            habit_list = ", ".join(habit_name)
            print(f"Your daily habits with the longest streak are '{habit_list}' with {streak} days.")
        else:
            print("There are no daily habits with a streak.")
        main_menu()

    elif choice == "Show longest streak for weekly habits":
        # Gets the weekly habits with the longest streak
        habit_name, streak = analyse.get_longest_streak_weekly()
        if habit_name:
            habit_list = ", ".join(habit_name)
            print(f"Your weekly habits with the longest streak are '{habit_list}' with {streak} weeks.")
        else:
            print("There are no weekly habits with a streak.")
        main_menu()

    elif choice == "Show longest streak for a specific habit":
        # Gets the longest streak of a given habit
        habits = db.get_all_habits()
        if not habits:
            print("Sorry, there are no habits to analyze.")
            main_menu()
            return
        habit_names = [habit['name'] for habit in habits]
        habit_name = questionary.select("Which habit do you want to analyze?", choices=habit_names).ask()

        habit_name, streak = analyse.get_longest_streak_by_name(habit_name)
        if streak:
            print(f"The longest streak for your habit '{habit_name}' is: {streak}")
        else:
            print(f"There is no streak for habit '{habit_name}'.")
        main_menu()

    elif choice == "Exit Analyse habits":
        main_menu()

def delete_habit_cli():
    # Define how habits can be deleted by the user
    habits = db.get_all_habits()
    if not habits:
        print("Sorry, there are no habits to delete.")
        main_menu()
        return

    habit_names = [habit['name'] for habit in habits]
    habit_name = questionary.select("Which habit do you want to delete?", choices=habit_names).ask()

    confirm_delete = questionary.confirm(f"Are you sure you want to delete '{habit_name}'? "
                                         "Habits once deleted cannot be restored.").ask()
    if confirm_delete:
        habit_id = db.get_habit_id(habit_name)
        db.delete_habit_from_table(habit_id)
        print(f"Your habit '{habit_name}' was deleted successfully!")
    else:
        print(f"Your habit '{habit_name}' was not deleted.")
    main_menu()

def exit_cli():
    # Exits the CLI
    print("See you next time!")
    exit()

if __name__ == "__main__":
    # Ask the user whether to load example data or not
    prompt_load_example_data()

    # Initialize the modules (with the correct current_db)
    initialize_modules()

    # Proceed to the main menu
    main_menu()