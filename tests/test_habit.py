import pytest
from datetime import datetime, timedelta
from habit import Habit


class TestHabit:
    def setup_method(self):
        # Setting up a common start date for all tests
        self.today = datetime(2025, 6, 2)
        # Creating a Habit instance with a specific start date
        self.habit = Habit("Exercise", "daily", self.today)

    def test_initialization_valid(self):
        # Verify that habit is initialized correctly with valid parameters
        assert self.habit.name == "Exercise"
        assert self.habit.periodicity == "daily"
        assert self.habit.start_date == self.today
        # Initially, no completion dates
        assert self.habit.get_completion_dates() == []

    def test_initialization_invalid_name(self):
        # Expect ValueError if habit name is empty
        with pytest.raises(ValueError):
            Habit("", "daily", self.today)

    def test_initialization_invalid_periodicity(self):
        # Expect ValueError if period is not specified
        with pytest.raises(ValueError):
            Habit("Exercise", "", self.today)

    def test_initialization_invalid_start_date(self):
        # Expect ValueError if start date isn't a proper date object
        with pytest.raises(ValueError):
            Habit("Exercise", "daily", "not-a-date")

    def test_mark_completed_valid(self):
        # Mark a valid completion on the next day and verify it's recorded
        next_day = self.today + timedelta(days=1)
        self.habit.mark_completed(next_day)
        assert self.habit.get_completion_dates() == [next_day]

    def test_mark_completed_duplicate_daily(self):
        # Mark habit completed twice on the same day; should raise an error
        self.habit.mark_completed(self.today)
        with pytest.raises(ValueError):
            self.habit.mark_completed(self.today)

    def test_mark_completed_before_start(self):
        # Attempt to mark completed before the habit start date
        with pytest.raises(ValueError):
            self.habit.mark_completed(self.today - timedelta(days=1))

    def test_mark_completed_duplicate_weekly(self):
        # For weekly habits, mark completion on the same week should raise
        habit = Habit("Gym workout", "weekly", self.today)
        habit.mark_completed(self.today)
        same_week = self.today + timedelta(days=3)
        with pytest.raises(ValueError):
            habit.mark_completed(same_week)

    def test_mark_completed_duplicate_monthly(self):
        # For monthly habits, marking twice in same month should raise
        habit = Habit("Planning", "monthly", self.today)
        habit.mark_completed(self.today)
        later_same_month = datetime(2025, 6, 28)
        with pytest.raises(ValueError):
            habit.mark_completed(later_same_month)

    def test_get_longest_streak_daily(self):
        # Test streak calculation for consecutive daily completions
        self.habit.mark_completed(self.today)
        self.habit.mark_completed(self.today + timedelta(days=1))
        self.habit.mark_completed(self.today + timedelta(days=2))
        # Longest streak should account for all consecutive days
        assert self.habit.get_longest_streak() == 3

    def test_get_longest_streak_weekly_same_year():
        # Test weekly streaks within the same year
        habit = Habit("Workout", "weekly", datetime(2025, 1, 1))
        habit.mark_completed(datetime(2025, 1, 1))
        habit.mark_completed(datetime(2025, 1, 8))
        habit.mark_completed(datetime(2025, 1, 15))
        assert habit.get_longest_streak() == 3

    def test_get_longest_streak_weekly_with_one_week_missed():
        # Check that missing a week affects streak calculation
        habit = Habit("Bike Ride", "weekly", datetime(2025, 1, 1))
        habit.mark_completed(datetime(2025, 1, 1))
        habit.mark_completed(datetime(2025, 1, 15))
        # Due to the gap, the longest streak is just 1
        assert habit.get_longest_streak() == 1

    def test_get_longest_streak_weekly_end_beginning_of_year():
        # Testing streaks crossing year boundary for weekly habits
        habit = Habit("Loundry", "weekly", datetime(2024, 12, 25))
        habit.mark_completed(datetime(2024, 12, 25))
        habit.mark_completed(datetime(2025, 1, 1))
        # Should count as a streak of 2, crossing year boundary
        assert habit.get_longest_streak() == 2

    def test_get_longest_streak_monthly(self):
        # Verify streak calculation over multiple months
        habit = Habit("Report", "monthly", datetime(2025, 1, 1))
        habit.mark_completed(datetime(2025, 1, 5))
        habit.mark_completed(datetime(2025, 2, 6))
        habit.mark_completed(datetime(2025, 3, 7))
        # Longest streak in this monthly pattern should be 3
        assert habit.get_longest_streak() == 3

    def test_get_streak_duration_string(self):
        # Check string formatting depending on periodicity
        assert self.habit.get_streak_duration_string(2) == "2 day(s)"
        self.habit.periodicity = "weekly"
        assert self.habit.get_streak_duration_string(2) == "2 week(s)"
        self.habit.periodicity = "monthly"
        assert self.habit.get_streak_duration_string(2) == "2 month(s)"

    def test_edit_habit_name_and_periodicity(self):
        # Verify editing of habit's core attributes
        self.habit.edit_habit(name="Read", periodicity="weekly")
        assert self.habit.name == "Read"
        assert self.habit.periodicity == "weekly"

    def test_edit_habit_start_date_removes_old_completions(self):
        # Changing start date should remove completions before new start
        old_date = self.today + timedelta(days=1)
        self.habit.mark_completed(old_date)
        new_start = self.today + timedelta(days=2)
        self.habit.edit_habit(start_date=new_start)
        # All completion dates should be >= new start date
        assert all(d >= new_start for d in self.habit.get_completion_dates())

    def test_repr_output(self):
        output = repr(self.habit)
        assert "Habit(name=" in output
        assert self.habit.name in output