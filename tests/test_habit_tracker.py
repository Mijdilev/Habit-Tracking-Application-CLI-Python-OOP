import pytest
from datetime import datetime, timedelta
from habit import Habit
from habit_tracker import HabitTracker


@pytest.fixture # Creates Habit type object for futher testing
def sample_habit():
    return Habit("Exercise", "daily", datetime.today())


@pytest.fixture # Creates HabitTracker type object for further testing
def tracker(sample_habit):
    tracker = HabitTracker()
    tracker.add_habit(sample_habit)
    return tracker


def test_add_habit(tracker, sample_habit):  # Tests adding a Habit object to the all habits list
    assert tracker.get_all_habits() == [sample_habit]


def test_add_invalid_habit(): # Tests adding a string instead of a Habit class instance to the list
    tracker = HabitTracker()
    with pytest.raises(TypeError):
        tracker.add_habit("not_a_habit")


def test_get_habits_by_periodicity(tracker): # Tests retrieving habits by periodicity
    result = tracker.get_habits_by_periodicity("daily")
    assert len(result) == 1
    assert result[0].name == "Exercise"


def test_get_habits_by_invalid_periodicity(tracker): # Tests how retrieving habits behaves when invalid periodicity was entered
    with pytest.raises(ValueError):
        tracker.get_habits_by_periodicity("Tomorrow")


def test_get_longest_streak_all_habits(tracker, sample_habit):
    today = sample_habit.start_date
    sample_habit.mark_completed(today)
    sample_habit.mark_completed(today + timedelta(days=1))
    assert tracker.get_longest_streak_all_habits() == 2


def test_get_longest_streak_for_habit(tracker, sample_habit):
    # Mark a habit as completed on its start date
    sample_habit.mark_completed(sample_habit.start_date)
    # Verify the longest streak for this specific habit
    assert tracker.get_longest_streak_for_habit("Exercise") == 1


def test_get_longest_streak_for_unknown_habit(tracker):
    # Test behavior when trying to get streak for a habit that doesn't exist
    assert tracker.get_longest_streak_for_habit("NonExistent") == 0


def test_edit_habit(tracker):
    new_start = datetime.today()
    # Edit the existing habit with new parameters
    tracker.edit_habit("Exercise", new_name="Workout", new_periodicity="weekly", new_start_date=new_start)
    habit = tracker.get_all_habits()[0]
    # Verify that the habit's parameters were updated correctly
    assert habit.name == "Workout"
    assert habit.periodicity == "weekly"
    assert habit.start_date == new_start


def test_edit_habit_invalid_name(tracker):
    # Test error when trying to edit with an invalid or empty name
    with pytest.raises(ValueError):
        tracker.edit_habit("Exercise", new_name="")


def test_edit_nonexistent_habit(tracker):
    # Ensure error is raised when trying to edit a habit that doesn't exist
    with pytest.raises(ValueError):
        tracker.edit_habit("NonExistent", new_name="NewName")


def test_delete_habit(tracker):
    # Delete a habit and check if it's removed from the tracker
    tracker.delete_habit("Exercise")
    assert tracker.get_all_habits() == []


def test_delete_nonexistent_habit(tracker):
    # Expect an error when trying to delete a habit that doesn't exist
    with pytest.raises(ValueError):
        tracker.delete_habit("Unknown")


def test_to_json(tracker):
    data = tracker.to_json()
    assert "habits" in data
    assert data["habits"][0]["name"] == "Exercise"


def test_from_json():
    # Create a sample data dictionary representing habits in JSON format
    data = {
        "habits": [
            {
                "name": "Read",
                "periodicity": "daily",
                "start_date": "2023-01-01",
                "completion_dates": ["2023-01-01", "2023-01-02"]
            }
        ]
    }
    tracker = HabitTracker.from_json(data)
    assert len(tracker.get_all_habits()) == 1
    habit = tracker.get_all_habits()[0]
    assert habit.name == "Read"
    assert len(habit.completion_dates) == 2
