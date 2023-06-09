# Task Record System
## Authors
- Dolendo, Jericho Paolo
- Festin, Angel Alexis
- Suñga, Rafael
## Description
This is a tasklisting application wherein you can lists tasks with deadlines and group them in categories.
## Usage
1. Important Notes
2. Dependencies
3. Features
### Important Notes:
- In order for the program to work, you should run the dump file first for users to appear and the application to work.
- There are users created for the handling of the application.
	username: appuser 		pass: user (used for clients)
	username: administrator 	pass: admin (used by admins)
- Use the app.py to run the program.
### Dependencies:
- mysql.connector (-m pip install mysql-connector-python)
### Features:
- Admin and user: There is an admin account and a starting user account made to interact with the database. 
    The user has select, delete, edit, and insert privileges.
    The amdimistrator user has all privileges.
- Alerts on missing input: If a user forgets to add an input, alerts will pop up to tell the user that they missed something.
- Login window: This is where users log in with their credentials in order to proceed to the main menu.
- Main menu: This is where users can access the exit, and choose whether the perform  operations on tasks or categories. Users may also return to the main menu.
- Task menu: This is where users can access functions related to Tasks. Users may also return to the main menu.
- Add Task: Adds a task based on the inputs of the user. The inputs are the Task name, description, duedate, category id, and whether or not the task is done. The id is automatically incremented.
- Delete Task: Deletes task by input id. 
- Edit task: Edits task by input id. You may edit the Task name, description, duedate, and category id.
- Mark as done: Sets the task to done by input id.
- View All tasks: Displays all tasks that are currently in the database.
- Category menu: This is where users can access functions related to Categories.
- Add Category: Adds a task based on the inputs of the user. The inputs are the Category name and description. The id is automatically incremented.
- Delete category: Deletes category by input id. 
- Edit category: Edits category by input id. The user may edit the Category name and description.
- View Categories: Displays all categories that are currently in the database.
- View Both: Displays both categories and tasks.



