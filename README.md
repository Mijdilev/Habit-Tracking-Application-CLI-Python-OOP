# Habit Tracker CLI Application

Welcome to Habit Tracker CLI! This console application helps you build and track beneficial habits. Monitor your goals on a daily, weekly, or monthly basis, analyze your progress, and stay motivated through streak tracking.


## Table of Contents

* [Features](#features)
* [How It Works](#how-it-works)
* [Installation](#installation)
  * [Requirements](#requirements)
  * [Step-by-Step Installation](#steb-by-step-istallation)
* [Usage](#usage)
  * [Running the Application](#running-the-application)
  * [Main menu](#main-menu)
  * [Basic Operations](#basic-operations)
* [Pytest Unit Tests](#pytest-unit-tests)
* [Error Handling](#error-handling)
* [Predifined habits data](#predefined-habits-data)
* [License](#license)

## Features
**Various Habit Definition:** Create habits with daily, weekly, or monthly periodicities.

**Command Line Interface:** Easy-to-use numbered menu system for all interactions.

**Completion Tracking:** Mark habits as completed on the current date or a custom date. The app prevents duplicate completions inside the same period (e.g., won't count a daily habit twice in one day).

**Streak Calculation:** Automatically calculates your longest consecutive streaks.

**Habit Management:** Add, edit (name, periodicity, start date), and delete habits.

**Data Storage:** All the habit data is saved locally in a JSON file.


## How It Works
* `habit.py`: Defines the `Habit` class, representing individual habits with their attributes and methods.
    
* `habit_tracker.py`: Defines the `HabitTracker` class, which manages a collection of `Habit` objects and provides opportunity to analyse their data.
   
* `main.py`: The main entry point for the CLI and user intaraction with the program, loading/saving data, and calling methods from `HabitTracker`.


## Istallation

### Requirements

* Python 3.10
* virtualenv (for dependency management)

### Steb-by-Step Istallation

1. Clone the repository:

```
https://github.com/Mijdilev/Habit-Tracking-Application-CLI-Python-OOP/
```
or use codespace on GitHub and create codespace on main.

2. This project uses standard python libraries. You can install them via pip if you don't have them already in your venv (e.g. pytest)

## Usage

### Running the Application

Run `main.py` file.

### Main menu

Here is the menu that will be displayed after you run the main file:

```
Main Menu
Habit Tracker Menu:
1. Add Habit
2. Mark Habit as Completed
3. List All Habits
4. List Habits by Periodicity
5. Get Longest Streak for All Habits
6. Get Longest Streak for a Habit
7. Edit/Delete Habit
8. Quit
```
### Basic Operations

1. **Adding a Habit**:
    - Select option 1
    - Enter the habit name
    - Choose periodicity
    - Set start date

2. **Marking Completion**:
    - Select option 2 
    - Choose a habit from the list
    - Specify completion date

3. **Viewing Statistics**:
    - Option 3: all habits
    - Option 4: filter by periodicity
    - Option 5: longest streak across all habits
    - Option 6: longest streak for specific habit
4. **Managing Habits**:
    - Option 7: edit or delete existing habits
    - Modify habit name, periodicity, or start date
    - Remove unwanted habits


### Pytest Unit tests
Inside the `tests` folder the pytest files `test_habit.py` and `test_habit_tracker.py` for testing the functionality of components `habit.py` and `habit_tracker.py` are contained.

To run the tests, open them in terminal and input: "pytest test_habit.py" or "pytest test_habit_tracker" and press "Enter" to see the results.

### Error Handling
The application includes error handling for:
* Invalid inpupt validation
* Date format verification
* File operations
* Duplicate entries prevention

### Predefined habits data
The application comes with a pre-configured set of test habits in `habits.json` . 

*Note:* You can remove this data by deleting these habits or the json file. The program should create a new one automatically.

## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/Mijdilev/Habit-Tracking-Application-CLI-Python-OOP/blob/main/LICENSE) file for details.