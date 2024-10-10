from datetime import datetime


class Habit:
    """Creating a class representing the habits."""

    def __init__(self, name: str, description: str, periodicity: str):
        """Initializing the habits.
        :param name: The name of the habit.
        :param description: A little description to the habit.
        :param periodicity: The frequency of the habit, daily or weekly.
        :param creation_date: The date and time the habit was created, default to the current date.
        :param checkoff_dates: List of the dates a habits got 'checked off', i.e. completed.
        """
        self.name = name
        self.description = description
        self.periodicity = periodicity
        self.creation_date = datetime.now()
        self.checkoff_dates = []

    # Access the parameters
    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_periodicity(self):
        return self.periodicity

    def get_creation_date(self):
        return self.creation_date

    def get_checkoff_dates(self):
        return self.checkoff_dates

    def checkoff_habit(self, checkoff_date: datetime = None) -> bool:
        """Attempt to check off the habit and return True if successful, False otherwise."""
        if not checkoff_date:
            checkoff_date = datetime.now()

        if self.checkoff_dates:
            last_checkoff = self.checkoff_dates[-1]
            if self.periodicity == "daily" and last_checkoff.date() == checkoff_date.date():
                return False
            elif self.periodicity == "weekly" and last_checkoff.isocalendar()[1] == checkoff_date.isocalendar()[1]:
                return False

        self.checkoff_dates.append(checkoff_date)
        return True # Habit was checked off successfully

    def edit_habit(self, new_name, new_description):
        """Defining how to edit names and descriptions of habits.
        :param new_name: The edited habit name.
        :param new_description: The edited habit description."""
        self.name = new_name
        self.description = new_description

    def streak(self):
        """Defining the calculation of the current streak when a habit gets checked off.
        Returns an int, which is the number of the currently checked off dates."""
        if not self.checkoff_dates:
            return 0

        sorted_checkoff_dates = sorted(set(self.checkoff_dates))
        current_streak = 1

        for i in range(len(sorted_checkoff_dates) -1, 0, -1):
            current = sorted_checkoff_dates[i]
            previous = sorted_checkoff_dates[i - 1]

            if self.periodicity == "daily":
                if (current - previous).days == 1:
                    current_streak += 1
                else:
                    break

            elif self.periodicity == "weekly":
                current_week = current.isocalendar()[1]
                previous_week = previous.isocalendar()[1]
                current_year = current.isocalendar()[0]
                previous_year = previous.isocalendar()[0]

                if (current_year == previous_year and current_week == previous_week + 1) or (
                        current_year == previous_year +1 and current_week == 1 and previous_week in {52, 53}):
                    current_streak += 1
                else:
                    break

        return current_streak

# Do I need a def __str__(self): representation here? (return f"{self.name}, ...)