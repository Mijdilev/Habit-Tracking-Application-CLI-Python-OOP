import json
from datetime import datetime, timedelta
from habit import Habit  # Assuming habit.py is in the same directory
from habit_tracker import HabitTracker  # Assuming habit_tracker.py is in the same directory


def load_data(filename="habits.json"):
    """
    Loads habits meta-data from a JSON file.
    If the file doesn't exist or is corrupted, it creates a new empty Habit Tracker.
    """
    try:
        with open(filename, "r") as f:
            data = json.load(f)  # Load JSON data from file
            return HabitTracker.from_json(data)  # Convert JSON data into a HabitTracker object
    except FileNotFoundError:
        print("No existing data found, creating a new Habit Tracker.")
        return HabitTracker()  # Return an empty tracker if the file doesn't exist
    except json.JSONDecodeError:
        print("Error decoding JSON. Creating a new Habit Tracker.")
        return HabitTracker()  # Return an empty tracker if the file is corrupted


def save_data(habit_tracker, filename="habits.json"):
    """
    Saves current habit data to a JSON file.
    Displays an error if there's an issue with file writing.
    """
    try:
        with open(filename, "w") as f:
            json.dump(habit_tracker.to_json(), f, indent=4)  # Save data in a nicely formatted JSON
    except Exception as e:
        print(f"An error occurred while saving data: {e}")


def get_habit_by_number(habit_tracker, prompt_message="Enter the number of the habit:"):
    """
    Displays a numbered list of habits and allows the user to select one by its number.
    Returns the selected Habit object or None if the input is invalid or no habits exist.
    """
    all_habits = habit_tracker.get_all_habits()  # Get the list of all habits
    if not all_habits:
        print("No habits tracked yet.")  # No habits, user can't select anything
        return None

    # Display all habits with numbers
    print("\n--- Your Habits ---")
    for i, habit in enumerate(all_habits):
        print(f"{i + 1}. {habit.name} (Periodicity: {habit.periodicity})")
    print("-------------------")

    while True:
        try:
            choice = input(prompt_message)  # Get user input
            habit_index = int(choice) - 1  # Convert choice to index
            if 0 <= habit_index < len(all_habits):
                return all_habits[habit_index]  # Return the selected habit
            else:
                print("Invalid number. Please choose from the list.")
        except ValueError:
            print("Invalid input. Please enter a number.")  # Input wasn't a valid number


def get_periodicity_choice():
    """
    Allows the user to choose a periodicity from a predefined list (daily, weekly, monthly).
    Continues to prompt until valid input is given.
    """
    print("\nSelect Periodicity:")
    print("1. Daily")
    print("2. Weekly")
    print("3. Monthly")
    while True:
        p_choice = input("Enter number for periodicity: ")
        if p_choice == '1':
            return "daily"
        elif p_choice == '2':
            return "weekly"
        elif p_choice == '3':
            return "monthly"
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


def get_date_choice(prompt_message="Enter date (YYYY-MM-DD):"):
    """
    Allows the user to choose a date: current date or a custom date.
    Ensures the custom date is valid and formatted correctly.
    """
    print("\nSelect Date Option:")
    print("1. Current Date")
    print("2. Custom Date")
    while True:
        date_option = input("Enter number for date option: ")
        if date_option == '1':
            return datetime.now()  # Current date
        elif date_option == '2':
            date_str = input(f"{prompt_message}: ")
            try:
                return datetime.strptime(date_str, "%Y-%m-%d")  # Parse custom date
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")
        else:
            print("Invalid choice. Please enter 1 or 2.")


def main():
    """
    Main function to run the Habit Tracker App with a simple text-based menu.
    Handles user input and calls appropriate actions based on their choice.
    """
    habit_tracker = load_data()  # Initialize the Habit Tracker from saved data (if it exists)

    while True:
        # Menu displayed to the user
        print("\nHabit Tracker Menu:")
        print("1. Add Habit")
        print("2. Mark Habit as Completed")
        print("3. List All Habits")
        print("4. List Habits by Periodicity")
        print("5. Get Longest Streak for All Habits")
        print("6. Get Longest Streak for a Habit")
        print("7. Edit/Delete Habit")
        print("8. Quit")

        choice = input("Enter your choice: ")

        try:
            if choice == "1":
                # Add a new habit
                name = input("Enter habit name: ")  # Get habit name
                periodicity = get_periodicity_choice()  # Get periodicity (daily, weekly, or monthly)

                # Choose start date for the new habit
                start_date_option = input("Select start date option (1. Current Date, 2. Custom Date): ")
                if start_date_option == '1':
                    start_date = datetime.now()
                elif start_date_option == '2':
                    date_str = input("Enter start date (YYYY-MM-DD): ")
                    start_date = datetime.strptime(date_str, "%Y-%m-%d")
                else:
                    print("Invalid option. Using current date as default.")
                    start_date = datetime.now()

                # Create and add the new habit
                habit = Habit(name, periodicity, start_date)
                habit_tracker.add_habit(habit)
                print("Habit added successfully.")

            elif choice == "2":
                # Mark a habit as completed for a specific date
                habit_to_mark = get_habit_by_number(habit_tracker, "Enter the number of the habit to mark completed:")
                if habit_to_mark:
                    completion_date = get_date_choice("Enter completion date (YYYY-MM-DD)")
                    try:
                        habit_to_mark.mark_completed(completion_date)  # Mark the habit as completed
                        print("Habit marked as completed.")
                    except ValueError as e:
                        print(f"Error: {e}")
                else:
                    print("No habit selected or found.")

            elif choice == "3":
                # Display all tracked habits
                all_habits = habit_tracker.get_all_habits()
                if all_habits:
                    print("\n--- All Habits ---")
                    for i, habit in enumerate(all_habits):
                        print(
                            f"{i + 1}. {habit.name} (Periodicity: {habit.periodicity}, Started: {habit.start_date.strftime('%Y-%m-%d')})")
                        # Display completion stats
                        if habit.completion_dates:
                            sorted_dates = sorted(habit.completion_dates)
                            print(f"   Last completed: {sorted_dates[-1].strftime('%Y-%m-%d')}")
                            print(f"   Completions: {[d.strftime('%Y-%m-%d') for d in sorted_dates]}")
                        else:
                            print("   No completions yet.")
                    print("-------------------")
                else:
                    print("No habits tracked yet.")


            elif choice == "8":
                # Exit the program and save any changes
                save_data(habit_tracker)
                print("Exiting Habit Tracker. Your data has been saved.")
                break

            else:
                print("Invalid choice. Please try again.")  # Invalid menu choice
        except ValueError as e:
            print(f"Invalid input: {e}. Please try again with correct format/options.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")  # Catch-all for unexpected errors


if __name__ == "__main__":
    main()