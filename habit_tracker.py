import json
from datetime import datetime
from habit import Habit


class HabitTracker:
    """
    Manages multiple Habit objects.
    """
    def __init__(self):
        """
        Initializes an empty list of habits.
        """
        self.habits = []

    def add_habit(self, habit):
        """
        Adds a new Habit object to the list.

        Params:
            habit (Habit): The Habit object to add.
        """
        if not isinstance(habit, Habit): # Rises TypeError when non-habit object was attempted to be added to the list
            raise TypeError("habit must be a Habit object.")
        self.habits.append(habit)

    def get_all_habits(self):
        """
        Returns a list of all Habit objects.
        """
        return self.habits

    def get_habits_by_periodicity(self, periodicity):
        """
        Returns a list of Habit objects that match the periodicity selected by user.

        Params:
            periodicity (str): The periodicity to filter by.
        """
        if not isinstance(periodicity, str) or not periodicity.strip():
            raise ValueError("Habit periodicity must be a non-empty string.")

        valid_periodicities = ["daily", "weekly", "monthly"] #Here all periodicities available for the program are listed
        if periodicity not in valid_periodicities:
            raise ValueError(f"Invalid periodicity: '{periodicity}'. Must be one of: {', '.join(valid_periodicities)}.")

        return [habit for habit in self.habits if habit.periodicity == periodicity]

    def get_longest_streak_all_habits(self):
        """
        Calculates and returns the longest streak among all habits.
        """
        if not self.habits:
            return 0
        return max(habit.get_longest_streak() for habit in self.habits)

    def get_longest_streak_for_habit(self, habit_name):
        """
        Returns the longest streak for a specific habit.

        Params:
            habit_name (str): The name of the habit.
        """
        if not isinstance(habit_name, str) or not habit_name.strip():
            raise ValueError("Habit name must be a non-empty string.")
        for habit in self.habits:
            if habit.name == habit_name:
                return habit.get_longest_streak()
        return 0

    def edit_habit(self, habit_name, new_name=None, new_periodicity=None, new_start_date=None):
        """
        Allows user to edit an existing habit.

        Params:
            habit_name (str): The name of the habit to edit.
            new_name (str, optional): The new name for the habit. Defaults to None.
            new_periodicity (str, optional): The new periodicity for the habit. Defaults to None.
            new_start_date (date, optional): The new start date for the habit. Defaults to None.
        """
        if not isinstance(habit_name, str) or not habit_name.strip():
            raise ValueError("Habit name must be a non-empty string.")
        for habit in self.habits:
            if habit.name == habit_name:
                if new_name is not None:
                    if not isinstance(new_name, str) or not new_name.strip():
                         raise ValueError("Habit name must be a non-empty string.")
                    habit.name = new_name
                if new_periodicity is not None:
                    if not isinstance(new_periodicity, str) or not new_periodicity.strip():
                        raise ValueError("Habit periodicity must be a non-empty string.")
                    habit.periodicity = new_periodicity
                if new_start_date is not None:
                    if not isinstance(new_start_date, datetime):
                        raise ValueError("Start date must be a datetime object.")
                    habit.start_date = new_start_date
                    if habit.completion_dates and any(date < new_start_date for date in habit.completion_dates):
                         habit.completion_dates = [
                            date for date in habit.completion_dates if date >= new_start_date
                        ]
                return
        raise ValueError(f"Habit with name '{habit_name}' not found.")  # Raise error if habit not found.

    def delete_habit(self, habit_name):
        """
        Deletes a habit.

        Params:
            habit_name (str): The name of the habit to delete.
        """
        if not isinstance(habit_name, str) or not habit_name.strip():
            raise ValueError("Habit name must be a non-empty string.")
        for index, habit in enumerate(self.habits):
            if habit.name == habit_name:
                del self.habits[index]
                return
        raise ValueError(f"Habit with name '{habit_name}' not found.")

    def to_json(self):
        """
        Converts the HabitTracker object to a JSON-serializable dictionary.
        """
        return {
            "habits": [
                {
                    "name": habit.name,
                    "periodicity": habit.periodicity,
                    "start_date": habit.start_date.strftime("%Y-%m-%d"),
                    "completion_dates": [date.strftime("%Y-%m-%d") for date in habit.completion_dates]
                }
                for habit in self.habits
            ]
        }

    @classmethod
    def from_json(cls, data):
        """
        Creates a HabitTracker object from a JSON-serializable dictionary.
        """
        habit_tracker = cls()
        for habit_data in data.get("habits", []):  #  .get() to handle missing "habits"
            try:  # try and except for error handling
                name = habit_data["name"]
                periodicity = habit_data["periodicity"]
                start_date = datetime.strptime(habit_data["start_date"], "%Y-%m-%d")
                completion_dates = [datetime.strptime(date_str, "%Y-%m-%d") for date_str in habit_data.get("completion_dates", [])] # Use .get()
                habit = Habit(name, periodicity, start_date)
                habit.completion_dates = completion_dates
                habit_tracker.add_habit(habit)
            except KeyError as e:
                print(f"Skipping habit due to missing key: {e}")
            except ValueError as e:
                print(f"Skipping habit due to invalid data: {e}")
        return habit_tracker