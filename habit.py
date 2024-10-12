from datetime import datetime


class Habit:
    """A class representing the habits."""

    def __init__(self, name: str, description: str, periodicity: str):
        """
        Initializing a new Habit instance .
        :param name: The name of the habit.
        :param description: A brief description of the habit.
        :param periodicity: The frequency of the habit, either 'daily' or 'weekly'.
        :param creation_date: The date and time the habit was created (automatically set).
        :param checkoff_dates: A list of the dates when a habit completed, i.e. 'checked off'.
        """
        self.name = name
        self.description = description
        self.periodicity = periodicity
        self.creation_date = datetime.now()
        self.checkoff_dates = []

    # Accessor methods
    def get_name(self):
        """Returns the name of the habit."""
        return self.name

    def get_description(self):
        """Returns the description of the habit."""
        return self.description

    def get_periodicity(self):
        """Returns the periodicity of the habit."""
        return self.periodicity

    def get_creation_date(self):
        """Returns the creation date of the habit."""
        return self.creation_date

    def get_checkoff_dates(self):
        """Returns the list of checkoff dates for the habit."""
        return self.checkoff_dates

    def checkoff_habit(self, checkoff_date: datetime = None) -> bool:
        """
        Attempts to check off the habit.
        :param checkoff_date: The date when the habit is checked off.
        :return: True if the habit was successfully checked off, False otherwise.
        """
        if not checkoff_date:
            checkoff_date = datetime.now()

        if self.checkoff_dates:
            last_checkoff = self.checkoff_dates[-1]
            if self.periodicity == "daily" and last_checkoff.date() == checkoff_date.date():
                return False # Already checked off today
            elif self.periodicity == "weekly" and last_checkoff.isocalendar()[1] == checkoff_date.isocalendar()[1]:
                return False # Already checked off this week

        self.checkoff_dates.append(checkoff_date)
        return True # Habit was checked off successfully

    def edit_habit(self, new_name, new_description):
        """
        Edit's the habits name and descriptions.
        :param new_name: The edited new habit name.
        :param new_description: The edited new habit description.
        """
        self.name = new_name
        self.description = new_description

    def streak(self):
        """
        Calculates the current streak of checkoff dates.

        :return: The number of the consecutive checkoffs for the habit.
        """
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

def __str__(self) -> str:
    """Returns a string representation of the habit."""
    return (f"Habit(name={self.name}, description={self.description}, periodicity={self.periodicity}, "
            f"creation_date={self.creation_date}, checkoff_dates={self.checkoff_dates})")