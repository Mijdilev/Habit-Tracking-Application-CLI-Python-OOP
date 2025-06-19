import json
from datetime import datetime
from habit import Habit


class HabitTracker:
    """
    Manages multiple Habit objects.
    """
    def __init__(self):
        """
        Creates an empty list to store habits.
        """
        self.habits = []

    def add_habit(self, habit):
        """
        Adds a habit to the list.

        Args:
            habit (Habit): The habit to add.
        """
        if not isinstance(habit, Habit):
            raise TypeError("habit must be a Habit object.")
        self.habits.append(habit)

    def get_all_habits(self):
        """
        Gets all habits.

        Returns:
            List of all Habit objects.
        """
        return self.habits

    def get_habits_by_periodicity(self, periodicity):
        """
        Finds habits with a specific periodicity.

        Args:
            periodicity (str): "daily", "weekly", or "monthly".

        Returns:
            List of habits matching the periodicity.
        """
        if not isinstance(periodicity, str) or not periodicity.strip():
            raise ValueError("Habit periodicity must be a non-empty string.")
        valid_periodicities = ["daily", "weekly", "monthly"]
        if periodicity not in valid_periodicities:
            raise ValueError(f"Invalid periodicity: '{periodicity}'. Must be one of: {', '.join(valid_periodicities)}.")
        return [habit for habit in self.habits if habit.periodicity == periodicity]

    def get_longest_streak_all_habits(self):
        """
        Finds the longest streak among all habits.

        Returns:
            Longest streak as integer.
        """
        if not self.habits:
            return 0
        return max(habit.get_longest_streak() for habit in self.habits)

    def get_longest_streak_for_habit(self, habit_name):
        """
        Finds the longest streak for a specific habit.

        Args:
            habit_name (str): The name of the habit.

        Returns:
            Longest streak for the habit or 0 if not found.
        """
        if not isinstance(habit_name, str) or not habit_name.strip():
            raise ValueError("Habit name must be a non-empty string.")
        for habit in self.habits:
            if habit.name == habit_name:
                return habit.get_longest_streak()
        return 0

    def edit_habit(self, habit_name, new_name=None, new_periodicity=None, new_start_date=None):
        """
        Edit details of an existing habit.

        Args:
            habit_name (str): Name of the habit to change.
            new_name (str, optional): New name.
            new_periodicity (str, optional): New periodicity.
            new_start_date (datetime, optional): New start date.
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
                    # Remove completion dates before new start date
                    if habit.completion_dates and any(date < new_start_date for date in habit.completion_dates):
                         habit.completion_dates = [
                            date for date in habit.completion_dates if date >= new_start_date
                        ]
                return
        raise ValueError(f"Habit with name '{habit_name}' not found.")

    def delete_habit(self, habit_name):
        """
        Removes a habit from the list.

        Args:
            habit_name (str): Name of the habit to delete.
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
        Converts habits to a JSON format.
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
        Creates a HabitTracker from saved data.

        Args:
            data (dict): Data with habits info.

        Returns:
            HabitTracker instance.
        """
        habit_tracker = cls()
        for habit_data in data.get("habits", []):
            try:
                name = habit_data["name"]
                periodicity = habit_data["periodicity"]
                start_date = datetime.strptime(habit_data["start_date"], "%Y-%m-%d")
                completion_dates = [
                    datetime.strptime(date_str, "%Y-%m-%d") for date_str in habit_data.get("completion_dates", [])
                ]
                habit = Habit(name, periodicity, start_date)
                habit.completion_dates = completion_dates
                habit_tracker.add_habit(habit)
            except KeyError as e:
                print(f"Skipping habit due to missing key: {e}")
            except ValueError as e:
                print(f"Skipping habit due to invalid data: {e}")
        return habit_tracker