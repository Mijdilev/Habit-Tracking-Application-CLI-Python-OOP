# Habit Tracker CLI Application

I'm glat to greet you in the the Habit Tracker CLI App! This is a simple and powerful command-line interface application designed to help you build and maintain consistent habits. You can track daily, weekly, or monthly goals, and analyse your progress with streak calculation functioanality.

## Table of Contents

* [Features](#features)
* [How It Works](#how-it-works)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
  * [Running the Application](#running-the-application)
* [Usage](#usage)
  * [Main Menu](#main-menu)
  * [Adding a Habit](#adding-a-habit)
  * [Marking a Habit as Completed](#marking-a-habit-as-completed)
  * [Listing Habits](#listing-habits)
  * [Checking Streaks](#checking-streaks)
  * [Editing/Deleting a Habit](#editingdeleting-a-habit)
* [Contributing](#contributing)
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


## Getting Started
Follow these steps to set up and run the Habit Tracker App on your local machine.

### Prerequisites
* Python 3.6 or higher installed on your system.

### Installation
1. Clone the repository:

```
https://github.com/Mijdilev/Habit-Tracking-Application-CLI-Python-OOP/
```


This project uses standard python libraries. You can install them via pip if you don't have them already (e.g. pytest)

### Running the Application

Run `main.py` file.

## Usage
Upon running the application, you'll see the main menu:

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
### Adding a Habit (Option 1)
1. Select 1 from the main menu.

2. Enter the habit's name.

3. Choose its periodicity by number (`1` for Daily, `2` for Weekly, `3` for Monthly).

4. Choose the start date option (`1` for Current Date, `2` for Custom Date).

### Marking a Habit as Completed (Option 2)
1. Select 2 from the main menu.

2. A numbered list of your habits will be displayed. Enter the number of the habit you wish to mark.

3. Choose the completion date option (`1` for Current Date, `2` for Custom Date).

*Note:* The app will prevent you from marking a habit as completed multiple times within its defined period (e.g., you can't mark a "daily" habit complete twice on the same day).

### Listing Habits (Options 3 & 4)
* List All Habits (Option 3): Displays every habit you are tracking, along with their data.

* List Habits by Periodicity (Option 4): You need to select for which periodicity you want to list your habits, then program displays all habits with choosen periodicity.

### Checking Streaks (Options 5 & 6)
* Get Longest Streak for All Habits (Option 5): Shows the single longest consecutive streak across all your habits.

* Get Longest Streak for a Habit (Option 6): You need to select a specific habit by typing its number and then app will display its longest streak, specifying the unit (days, weeks, or months).

### Editing/Deleting a Habit (Option 7)
1. Select 7 from the main menu.

2. A numbered list of your habits will be displayed. Enter the number of the habit you wish to modify or delete.

3. Choose whether to 1. Edit Habit or 2. Delete Habit.

   * If Editing: You'll be prompted for a new name (press Enter to keep old), new periodicity (select by number, or 1 to keep old), and new start date (select by number, or 1 to keep old).

   * If Deleting: You'll be asked for confirmation before the habit is permanently removed.

  
## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/Mijdilev/Habit-Tracking-Application-CLI-Python-OOP/blob/main/LICENSE) file for details.