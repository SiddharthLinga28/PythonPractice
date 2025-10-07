Hard2
Expense Tracker (CLI)

This is a simple command-line application for tracking expenses, setting monthly budgets by category, and getting quick alerts if you overspend (if you’ve reached or exceeded your budget limit). It stores expenses in CSV (Comma Separated Value) format and lets you store your budgets in a simple JSON file. You do not need to install any external libraries.

Why
So you can track how you spend your money without messing around with spreadsheets. You can add an expense in the app and quickly run a monthly report to review and see if you went over your budget.

Requirements
• Python 3.x (And you will NOT need to install any external packages to run this code)
 
How to run
Save this project code in a folder.

Run the following command: python expense_tracker.py
The application will generate the following files:
• expenses.csv – the file that will be the log of your expenses, consisting of the following columns: date, amount, category, and note
• budgets.json – your monthly budgets by category

Main Commands (in the menu)
Add expense — specify the date (YYYY-MM-DD, leave empty for today), enter an amount, specify a category, and optionally enter a note.
Show recent expenses — displays the last N entries.
Monthly report — displays totals, number of transactions, average size of transaction, spending by category, alerts if you’ve overspent on a category, and display the top 5 expenses (for a specific month specified by YYYY-MM, or the current month).
Category report — display totals by month for a specific category, or display total for all time when the category is left blank.
Set monthly budget — enter a budget cap on a monthly basis for a specific category. For example, Food = 250.
Show budgets — displays your budgets.
Exit — exits the program.

Categories
Default categories are: Food, Rent, Transport, Utilities, Health, Education, Entertainment, Other. Categories that do not match one of the defaults are added to a list on first use.