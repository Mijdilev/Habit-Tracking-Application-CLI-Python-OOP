import json
from datetime import datetime, timedelta
from habit import Habit  # Assuming habit.py is in the same directory
from habit_tracker import HabitTracker  # Assuming habit_tracker.py is in the same directory


def load_data(filename="habits.json"):
    """
    Loads habaits meta-data from a JSON file.
    """
    try:
        with open(filename, "r") as f:
            data = json.load(f)
            return HabitTracker.from_json(data)
    except FileNotFoundError:
        print("No existing data found, creating a new Habit Tracker.")
        return HabitTracker()
    except json.JSONDecodeError:
        print("Error decoding JSON. Creating a new Habit Tracker.")
        return HabitTracker()


def save_data(habit_tracker, filename="habits.json"):
    """
    Saves habit data to a JSON file.
    """
    try:
        with open(filename, "w") as f:
            json.dump(habit_tracker.to_json(), f, indent=4)
    except Exception as e:
        print(f"An error occurred while saving data: {e}")


def get_habit_by_number(habit_tracker, prompt_message="Enter the number of the habit:"):
    """
    Helper function to display numbered list of habits and provide user's habit selection by number.

    Returns the selected Habit object or None if invalid input/no habits.
    """
    all_habits = habit_tracker.get_all_habits()
    if not all_habits:
        print("No habits tracked yet.")
        return None

    print("\n--- Your Habits ---")
    for i, habit in enumerate(all_habits):
        print(f"{i + 1}. {habit.name} (Periodicity: {habit.periodicity})")
    print("-------------------")

    while True:
        try:
            choice = input(prompt_message)
            habit_index = int(choice) - 1
            if 0 <= habit_index < len(all_habits):
                return all_habits[habit_index]
            else:
                print("Invalid number. Please choose from the list.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def get_periodicity_choice():
    """Helper function that allows user to choose periodicities from the numerated list."""
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

    """Helper function that allows user to select an oprion for date input (current or custom)."""

    print("\nSelect Date Option:")
    print("1. Current Date")
    print("2. Custom Date")
    while True:
        date_option = input("Enter number for date option: ")
        if date_option == '1':
            return datetime.now()
        elif date_option == '2':
            date_str = input(f"{prompt_message}: ")
            try:
                return datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")
        else:
            print("Invalid choice. Please enter 1 or 2.")


def main():
    """
    Main function to run the Habit Tracker App with a CLI.
    """
    habit_tracker = load_data()

    while True: #Showing the menu where user can interect with the program
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
                # 1. Add Habit option.
                name = input("Enter habit name: ")
                periodicity = get_periodicity_choice()  # calls helper function to allow user choose a periodicity

                start_date_option = input("Select start date option (1. Current Date, 2. Custom Date): ") # calls helper function to allow user choose a date option
                if start_date_option == '1':
                    start_date = datetime.now()
                elif start_date_option == '2':
                    date_str = input("Enter start date (YYYY-MM-DD): ")
                    start_date = datetime.strptime(date_str, "%Y-%m-%d")
                else:
                    print("Invalid option. Using current date as default.")
                    start_date = datetime.now()

                habit = Habit(name, periodicity, start_date)
                habit_tracker.add_habit(habit)
                print("Habit added successfully.")

            elif choice == "2":
                # 2. Mark Habit as Completed option.
                habit_to_mark = get_habit_by_number(habit_tracker, "Enter the number of the habit to mark completed:")
                if habit_to_mark:
                    completion_date = get_date_choice("Enter completion date (YYYY-MM-DD)")  # calls helper function to allow user choose a date option
                    try:
                        habit_to_mark.mark_completed(completion_date)
                        print("Habit marked as completed.")
                    except ValueError as e:
                        print(f"Error: {e}")
                else:
                    print("No habit selected or found.")

            elif choice == "3":
                #3. Get all habits option.
                all_habits = habit_tracker.get_all_habits()
                if all_habits:
                    print("\n--- All Habits ---")
                    for i, habit in enumerate(all_habits):
                        print(
                            f"{i + 1}. {habit.name} (Periodicity: {habit.periodicity}, Started: {habit.start_date.strftime('%Y-%m-%d')})")
                        if habit.completion_dates:
                            sorted_dates = sorted(habit.completion_dates)
                            print(f"   Last completed: {sorted_dates[-1].strftime('%Y-%m-%d')}")
                            print(f"   Completions: {[d.strftime('%Y-%m-%d') for d in sorted_dates]}")
                        else:
                            print("   No completions yet.")
                    print("-------------------")
                else:
                    print("No habits tracked yet.")

            elif choice == "4":
                # 4. Get habit by periodicity option
                periodicity = get_periodicity_choice()  # calls helper function to allow user choose a periodicity option
                habits_by_periodicity = habit_tracker.get_habits_by_periodicity(periodicity)
                if habits_by_periodicity:
                    print(f"\n--- Habits with periodicity '{periodicity}' ---")
                    for i, habit in enumerate(habits_by_periodicity):
                        print(f"{i + 1}. {habit.name} (Started: {habit.start_date.strftime('%Y-%m-%d')})")
                    print("-------------------")
                else:
                    print(f"No habits found with periodicity '{periodicity}'.")

            elif choice == "5":
                # 5. Get longest streak of all habits option.
                longest_streak = habit_tracker.get_longest_streak_all_habits()
                if longest_streak > 0:
                    print(
                        f"Longest streak across all habits: {longest_streak} units (could be days, weeks, or months depending on habit type)")
                    #uses word "units" because periodicities may differ across all habits.
                else:
                    print("No streaks found yet.")

            elif choice == "6":
                # 6. Get Longest Streak for a Specific Habit option.
                habit_to_check = get_habit_by_number(habit_tracker,
                                                     "Enter the number of the habit to check streak for:") # calls helper function to allow user choose a habit by number
                if habit_to_check:
                    longest_streak = habit_to_check.get_longest_streak()
                    print(
                        f"Longest streak for habit '{habit_to_check.name}': {habit_to_check.get_streak_duration_string(longest_streak)}")
                else:
                    print("No habit selected or found.")


            elif choice == "7":
                # 7. Edit/Delete Habit option.
                habit_to_modify = get_habit_by_number(habit_tracker, "Enter the number of the habit to edit/delete:")
                if not habit_to_modify:
                    print("No habit selected or found.")
                    continue

                print(f"\nSelected Habit: {habit_to_modify.name}") #Prompt user to choose the number of the next action: to Edit or to Delete habit.
                print("1. Edit Habit")
                print("2. Delete Habit")
                edit_choice = input("Enter your choice: ")

                if edit_choice == "1":
                    new_name = None
                    periodicity_choice = None
                    new_start_date = None

                    # Edit Name of a habit
                    name_option = input(f"Current name: '{habit_to_modify.name}'. Enter 1 to keep, 2 to enter new: ")
                    if name_option == '2':
                        new_name = input("Enter the new name: ")
                        if not new_name.strip():  # Prevent setting empty name
                            print("Name cannot be empty. Keeping old name.")
                            new_name = None

                    # Edit Periodicity of a habit
                    print(f"Current periodicity: '{habit_to_modify.periodicity}'.")
                    print("Select new periodicity:")
                    print("1. Keep old periodicity") # This option allows user to left the periodicity unchanged
                    print("2. Daily")
                    print("3. Weekly")
                    print("4. Monthly")
                    p_option = input("Enter number for periodicity: ")
                    if p_option == '1':
                        periodicity_choice = None  # Keeps old periodicity
                    elif p_option == '2':
                        periodicity_choice = "daily"
                    elif p_option == '3':
                        periodicity_choice = "weekly"
                    elif p_option == '4':
                        periodicity_choice = "monthly"
                    else:
                        print("Invalid option. Keeping old periodicity.")
                        periodicity_choice = None

                    # Edit Start Date of a habit
                    print(f"Current start date: '{habit_to_modify.start_date.strftime('%Y-%m-%d')}'.")
                    print("Select new start date option:")
                    print("1. Keep old date") # This option allows user to left the date unchanged
                    print("2. Current Date")
                    print("3. Custom Date (YYYY-MM-DD)")
                    date_option = input("Enter number for start date option: ")
                    if date_option == '1':
                        new_start_date = None  # Keeps old date
                    elif date_option == '2':
                        new_start_date = datetime.now()
                    elif date_option == '3':
                        date_str = input("Enter custom start date (YYYY-MM-DD): ")
                        try:
                            new_start_date = datetime.strptime(date_str, "%Y-%m-%d")
                        except ValueError:
                            print("Invalid date format. Keeping old date.")
                            new_start_date = None
                    else:
                        print("Invalid option. Keeping old date.")
                        new_start_date = None

                    try:
                        habit_tracker.edit_habit(
                            habit_name=habit_to_modify.name,  # Use existing name to find it
                            new_name=new_name,
                            new_periodicity=periodicity_choice,
                            new_start_date=new_start_date
                        )
                        print("Habit edited successfully.")
                    except ValueError as e:
                        print(f"Error: {e}")

                elif edit_choice == "2":
                    try:
                        habit_tracker.delete_habit(habit_to_modify.name)  # Deletes selected habit
                        print("Habit deleted successfully.")
                    except ValueError as e:
                        print(f"Error: {e}")
                else:
                    print("Invalid choice. Please try again.")

            elif choice == "8":
                # 8. Exits the program with saving all changes maded.
                save_data(habit_tracker)
                print("Exiting Habit Tracker. Your data has been saved.")
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError as e:
            print(f"Invalid input: {e}. Please try again with correct format/options.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()