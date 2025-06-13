import pytest
from datetime import datetime, timedelta
from habit import Habit


class TestHabit:

    def setup_method(self):
        self.today = datetime(2025, 6, 2)
        self.habit = Habit("Exercise", "daily", self.today)

    def test_initialization_valid(self):
        assert self.habit.name == "Exercise"
        assert self.habit.periodicity == "daily"
        assert self.habit.start_date == self.today
        assert self.habit.get_completion_dates() == []

    def test_initialization_invalid_name(self):
        with pytest.raises(ValueError):
            Habit("", "daily", self.today)

    def test_initialization_invalid_periodicity(self):
        with pytest.raises(ValueError):
            Habit("Exercise", "", self.today)

    def test_initialization_invalid_start_date(self):
        with pytest.raises(ValueError):
            Habit("Exercise", "daily", "not-a-date")

    def test_mark_completed_valid(self):
        next_day = self.today + timedelta(days=1)
        self.habit.mark_completed(next_day)
        assert self.habit.get_completion_dates() == [next_day]

    def test_mark_completed_duplicate_daily(self):
        self.habit.mark_completed(self.today)
        with pytest.raises(ValueError):
            self.habit.mark_completed(self.today)

    def test_mark_completed_before_start(self):
        with pytest.raises(ValueError):
            self.habit.mark_completed(self.today - timedelta(days=1))

    def test_mark_completed_duplicate_weekly(self):
        habit = Habit("Jog", "weekly", self.today)
        habit.mark_completed(self.today)
        same_week = self.today + timedelta(days=3)
        with pytest.raises(ValueError):
            habit.mark_completed(same_week)

    def test_mark_completed_duplicate_monthly(self):
        habit = Habit("Budget", "monthly", self.today)
        habit.mark_completed(self.today)
        later_same_month = datetime(2025, 6, 28)
        with pytest.raises(ValueError):
            habit.mark_completed(later_same_month)

    def test_get_longest_streak_daily(self):
        self.habit.mark_completed(self.today)
        self.habit.mark_completed(self.today + timedelta(days=1))
        self.habit.mark_completed(self.today + timedelta(days=2))
        assert self.habit.get_longest_streak() == 3

    def test_get_longest_streak_weekly(self):
        habit = Habit("Walk", "weekly", self.today)
        habit.mark_completed(self.today)
        habit.mark_completed(self.today + timedelta(days=7))
        habit.mark_completed(self.today + timedelta(days=14))
        assert habit.get_longest_streak() == 3

    def test_get_longest_streak_monthly(self):
        habit = Habit("Report", "monthly", datetime(2025, 1, 1))
        habit.mark_completed(datetime(2025, 1, 5))
        habit.mark_completed(datetime(2025, 2, 6))
        habit.mark_completed(datetime(2025, 3, 7))
        assert habit.get_longest_streak() == 3

    def test_get_streak_duration_string(self):
        assert self.habit.get_streak_duration_string(2) == "2 day(s)"
        self.habit.periodicity = "weekly"
        assert self.habit.get_streak_duration_string(2) == "2 week(s)"
        self.habit.periodicity = "monthly"
        assert self.habit.get_streak_duration_string(2) == "2 month(s)"

    def test_edit_habit_name_and_periodicity(self):
        self.habit.edit_habit(name="Read", periodicity="weekly")
        assert self.habit.name == "Read"
        assert self.habit.periodicity == "weekly"

    def test_edit_habit_start_date_removes_old_completions(self):
        old_date = self.today + timedelta(days=1)
        self.habit.mark_completed(old_date)
        new_start = self.today + timedelta(days=2)
        self.habit.edit_habit(start_date=new_start)
        assert all(d >= new_start for d in self.habit.get_completion_dates())

    def test_repr_output(self):
        output = repr(self.habit)
        assert "Habit(name=" in output
        assert self.habit.name in output



