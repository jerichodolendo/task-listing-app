from distutils.log import info
from re import I
from select import select
from tkinter import *
from tkinter import messagebox
from turtle import width
from typing import Any
import mysql.connector

# initializes login window
root = Tk()
root.title('NotesDB')
root.geometry("315x345")
root.configure(bg="#ffe8b8")
root.resizable(False,False)

# validates password and username
def validate_credentials(user_name,pass_word):
    try:
        global db
        db = mysql.connector.connect(
        host="localhost",
        user=user_name.get(),
        password=pass_word.get(),
        port='3306'
        )     
    except:
        print("Connection Unsuccesful")
        root.destroy()
    else:
        print("Connection Succesful")
        root.destroy()
        main_menu_function()

# initializes login window
login_frame = LabelFrame(root, text="Login", bg="#ffe8b8")
login_frame.pack(ipady=105)

user_name_label = Label(login_frame, text="User Name", bg="#ffe8b8")
user_name_label.pack(pady=10)
user_name = StringVar()
user_name_entry = Entry(login_frame, textvariable=user_name)
user_name_entry.pack(ipadx=50, padx=45)

pass_word_label = Label(login_frame, text="Password", bg="#ffe8b8")
pass_word_label.pack(pady=10)
pass_word = StringVar()
pass_word_entry = Entry(login_frame, textvariable=pass_word, show='*')
pass_word_entry.pack(ipadx=50, padx=45)

login_button = Button(login_frame, text="Login", width=30, command=lambda:validate_credentials(user_name,pass_word))
login_button.pack(pady=20)

# displays main menu
def main_menu_function():
    global db
    global main_menu_window
    global view_all_tasks_frame
    global view_all_categories_frame

    mariadb = db.cursor()

    mariadb.execute("CREATE DATABASE IF NOT EXISTS `task-listing`")
    mariadb.execute("USE `task-listing`")
    mariadb.execute("""CREATE TABLE IF NOT EXISTS `category`(
            `categoryid` INT(5) NOT NULL AUTO_INCREMENT, 
            `categoryname` VARCHAR(32) NOT NULL, 
            `categorydesc` VARCHAR(256),
            PRIMARY KEY(`categoryid`))
            """)
    mariadb.execute("""
        CREATE TABLE IF NOT EXISTS `task`( 
            `taskid` INT(5) NOT NULL AUTO_INCREMENT,
            `isdone` BOOLEAN NOT NULL,
            `taskname` VARCHAR(32) NOT NULL,
            `taskdesc` VARCHAR(256),
            `adddate` DATE NOT NULL,
            `duedate` DATE,
            `categoryid` INT(5),
            KEY `task_catid_fk` (`categoryid`),
            PRIMARY KEY(`taskid`),
            CONSTRAINT `task_catid_fk` FOREIGN KEY (`categoryid`)
            REFERENCES `category` (`categoryid`));
    """)

    db.commit()

    main_menu_window = Tk()
    main_menu_window.title('NotesDB')
    main_menu_window.configure(bg="#ffe8b8")

    main_menu_frame = LabelFrame(main_menu_window, text="Main Menu", bg="#ffe8b8")
    main_menu_frame.pack(fill="both",expand="yes")

    task_button = Button(main_menu_frame, text="Task", command=task_function)
    task_button.pack(pady=5, padx=10, ipadx=107)

    category_button = Button(main_menu_frame, text="Category", command=category_function)
    category_button.pack(pady=5, padx=10, ipadx=94)

    exit_button = Button(main_menu_frame, text="Exit", command=exit_app)
    exit_button.pack(pady=5, padx=10, ipadx=108)

    view_all_tasks_frame = LabelFrame(main_menu_window, text="Current Tasks", bg="#ffe8b8")
    view_all_tasks_frame.pack(fill="both")

    view_all_categories_frame = LabelFrame(main_menu_window, text="Categories", bg="#ffe8b8")
    view_all_categories_frame.pack(fill="both")

    show_tasks(view_all_tasks_frame)
    show_categories(view_all_categories_frame)
    mariadb.close()

# quits the application
def exit_app():
    global db
    db.close()

    main_menu_window.destroy()
    root.quit()

# returns to main menu
def return_to_menu(window):
    for label in view_all_tasks_frame.grid_slaves():
        label.grid_forget()

    for label in view_all_categories_frame.grid_slaves():
        label.grid_forget()

    show_tasks(view_all_tasks_frame)
    show_categories(view_all_categories_frame)

    window.destroy()
    main_menu_window.deiconify()

# submits task details
def submit_task():
    global db
    global add_taskname_textbox
    global add_taskdesc_textbox
    global add_duedate_textbox
    global add_taskdone_textbox
    global add_category_textbox
    
    def get_bool(string):
        eval_str = string
        if(eval_str.lower() == 'yes'):
            return '1'
        elif(eval_str.lower() == 'no'):
            return '0'
    
    bool_task = get_bool(add_taskdone_textbox.get())
    
    if(len(add_taskname_textbox.get()) == 0 or (bool_task != "1" or "0")):
            alert('Task Name or Task Progress is Empty')
            return

    mariadb = db.cursor()

    mariadb.execute("USE `task-listing`;")
    mariadb.execute("""INSERT INTO `task` (taskname, taskdesc, adddate, duedate, isdone, categoryid)
    VALUES (%(taskname)s, %(taskdesc)s, CURDATE(), %(duedate)s, %(isdone)s, %(categoryid)s)""",
    {
        'taskname': add_taskname_textbox.get(),
        'taskdesc': add_taskdesc_textbox.get(),
        'duedate': add_duedate_textbox.get(),
        'isdone': bool_task,
        'categoryid': add_category_textbox.get()
    })

    db.commit()
    mariadb.close()

    add_taskname_textbox.delete(0,END)
    add_taskdesc_textbox.delete(0,END)
    add_duedate_textbox.delete(0,END)
    add_taskdone_textbox.delete(0,END)
    add_category_textbox.delete(0,END)

    show_tasks(view_all_tasks_frame)
    return_to_menu(task_window)

# deletes task
def delete_task():
    global db
    global taskid_select_textbox

    if(len(taskid_select_textbox.get())== 0):
        alert('Task ID is Empty')
        return
    
    mariadb = db.cursor()

    mariadb.execute("USE `task-listing`")
    mariadb.execute("DELETE FROM `task` WHERE taskid = %(taskid)s",
    {
        'taskid': taskid_select_textbox.get()
    }
    )

    db.commit()
    mariadb.close()

    taskid_select_textbox.delete(0,END)
    return_to_menu(task_window)

# marks a task as done
def mark_as_done():
    global db
    global taskid_select_textbox

    if(len(taskid_select_textbox.get())== 0):
        alert('Task ID is Empty')
        return

    mariadb = db.cursor()

    mariadb.execute("USE `task-listing`")
    mariadb.execute("SELECT `isdone` FROM `task` WHERE taskid = %(taskid)s",
    {
        'taskid': taskid_select_textbox.get()
    }
    )

    isdone = mariadb.fetchone()[0]

    if(isdone == 1):
        alert('Task is Already Done')
        mariadb.close()
        return
    
    mariadb.execute('UPDATE `task` SET isdone = 1 WHERE taskid = %(taskid)s',
    {
        'taskid': taskid_select_textbox.get()
    }
    )

    db.commit()
    mariadb.close()

    taskid_select_textbox.delete(0,END)
    return_to_menu(task_window)

# displays both tasks and categories
def view_both():
    view_window = Tk()
    view_window.title("NotesDB")
    view_window.configure(bg="#ffe8b8")

    list_tasks_frame = LabelFrame(view_window, text="Current Tasks", bg="#ffe8b8")
    list_tasks_frame.pack(fill="both")

    list_categories_frame = LabelFrame(view_window, text="Categories", bg="#ffe8b8")
    list_categories_frame.pack(fill="both")

    close_button = Button(view_window, text="Close Window", width=30, command=lambda:view_window.destroy())
    close_button.pack(pady=14)

    show_tasks(list_tasks_frame)
    show_categories(list_categories_frame)

# initializes task window and its functions
def task_function():
    global add_taskname_textbox
    global add_taskdesc_textbox
    global add_duedate_textbox
    global add_category_textbox
    global add_taskdone_textbox
    global taskid_select_textbox
    global task_window

    main_menu_window.withdraw()

    task_window = Tk()
    task_window.title("NotesDB")
    task_window.configure(bg="#ffe8b8")

    task_frame = LabelFrame(task_window, text="Task Menu", bg="#ffe8b8")
    task_frame.pack()

    add_taskname_textbox = Entry(task_frame, width=30)
    add_taskname_textbox.grid(row=0, column=1, padx=20, pady=(10, 0))
    add_taskname_label = Label(task_frame, text="Task Name: ", bg="#ffe8b8")
    add_taskname_label.grid(row=0, column=0, pady=(10, 0), ipadx=20)

    add_taskdesc_textbox = Entry(task_frame, width=30)
    add_taskdesc_textbox.grid(row=1, column=1, padx=20, pady=(10, 0))
    add_taskdesc_label = Label(task_frame, text="Task Desc.: ", bg="#ffe8b8")
    add_taskdesc_label.grid(row=1, column=0, pady=(10, 0), ipadx=20)

    add_duedate_textbox = Entry(task_frame, width=30)
    add_duedate_textbox.grid(row=2, column=1, padx=20, pady=(10, 0))
    add_duedate_textbox.insert(0,"yy-mm-dd")
    add_duedate_label = Label(task_frame, text="Due Date: ", bg="#ffe8b8")
    add_duedate_label.grid(row=2, column=0, pady=(10, 0), ipadx=20)

    add_category_textbox = Entry(task_frame, width=30)
    add_category_textbox.grid(row=3, column=1, padx=20, pady=(10, 0))
    add_categoryid_label = Label(task_frame, text="Category ID: ", bg="#ffe8b8")
    add_categoryid_label.grid(row=3, column=0, pady=(10, 5))

    add_taskdone_textbox = Entry(task_frame, width=30)
    add_taskdone_textbox.grid(row=4, column=1, padx=20, pady=(10, 0))
    add_taskdone_textbox.insert(0,"Yes/No")
    add_taskdone_label = Label(task_frame, text="Task Done: ", bg="#ffe8b8")
    add_taskdone_label.grid(row=4, column=0, pady=(10, 5))

    task_addbutton = Button(task_frame, text="Add Task", command=submit_task)
    task_addbutton.grid(row=5, column=0, columnspan=2, pady=5, padx=10, ipadx=100)

    task_viewbutton = Button(task_frame, text="View All Tasks", command=view_both)
    task_viewbutton.grid(row=6, column=0, columnspan=2, pady=5, padx=10, ipadx=87)

    taskid_select_textbox = Entry(task_frame, width=30)
    taskid_select_textbox.grid(row=7, column=1, pady=(5, 5))
    taskid_select_label = Label(task_frame, text="Select ID: ", bg="#ffe8b8")
    taskid_select_label.grid(row=7, column=0, ipadx=20, pady=(5, 5))
    
    task_editbutton = Button(task_frame, text="Edit Task", command=edit_task_function)
    task_editbutton.grid(row=8, column=0, columnspan=2, pady=5, padx=10, ipadx=101)

    task_markdone = Button(task_frame, text="Mark As Done", command=mark_as_done)
    task_markdone.grid(row=9, column=0, columnspan=2, pady=5, padx=10, ipadx=87)

    task_deletebutton = Button(task_frame, text="Delete Task", command=delete_task)
    task_deletebutton.grid(row=10, column=0, columnspan=2, pady=5, padx=10, ipadx=94)

    task_returnbutton = Button(task_frame, text="Exit to Menu",command=lambda: return_to_menu(task_window))
    task_returnbutton.grid(row=11, column=0, columnspan=2, pady=5, padx=10, ipadx=90)

# submits task edits
def edit_task():
    global db
    global edit_task_window
    global edit_taskname_textbox
    global edit_taskdesc_textbox
    global edit_duedate_textbox
    global edit_categoryid_textbox
    global edit_taskdone_textbox
    global edit_task_id

    mariadb = db.cursor()

    def get_bool(string):
        eval_str = string
        if(eval_str.lower() == 'yes'):
            return '1'
        elif(eval_str.lower() == 'no'):
            return '0'

    mariadb.execute("USE `task-listing`;")
    mariadb.execute("""UPDATE task SET
        `taskname` = %(taskname)s,
        `taskdesc` = %(taskdesc)s,
        `duedate` = %(duedate)s,
        `isdone` = %(isdone)s,
        `categoryid` = %(categoryid)s
        WHERE taskid = %(taskid)s   
    """,
    {
        'taskname': edit_taskname_textbox.get(),
        'taskdesc': edit_taskdesc_textbox.get(),
        'duedate': edit_duedate_textbox.get(),
        'isdone': get_bool(edit_taskdone_textbox.get()),
        'categoryid': edit_categoryid_textbox.get(),
        'taskid': edit_task_id
    }
    )

    db.commit()
    mariadb.close()

    edit_taskname_textbox.delete(0,END)
    edit_taskdesc_textbox.delete(0,END)
    edit_duedate_textbox.delete(0,END)
    edit_taskdone_textbox.delete(0,END)
    edit_categoryid_textbox.delete(0,END)

    edit_task_window.destroy()    
    task_function()

# initializes task editor window
def edit_task_function():
    global db
    global taskid_select_textbox
    global edit_task_id
    global edit_task_window
    global edit_taskname_textbox
    global edit_taskdesc_textbox
    global edit_duedate_textbox
    global edit_categoryid_textbox
    global edit_taskdone_textbox
    
    edit_task_id = taskid_select_textbox.get()

    if(len(edit_task_id)== 0):
        alert('Task ID is Empty')
        return

    task_window.withdraw()

    edit_task_window = Tk()
    edit_task_window.title("NotesDB")
    edit_task_window.configure(bg="#ffe8b8")

    edit_task_frame = LabelFrame(edit_task_window, text="Edit Task", bg="#ffe8b8")
    edit_task_frame.pack(fill="both")

    # Edit Task text boxes
    edit_taskname_textbox = Entry(edit_task_frame, width=30)
    edit_taskname_textbox.grid(row=0, column=1, padx=20, pady=(10, 0))
    edit_taskname_label = Label(edit_task_frame, text="Task Name: ", bg="#ffe8b8")
    edit_taskname_label.grid(row=0, column=0, pady=(10, 0), ipadx=20)

    edit_taskdesc_textbox = Entry(edit_task_frame, width=30)
    edit_taskdesc_textbox.grid(row=1, column=1, padx=20, pady=(10, 0))
    edit_taskdesc_label = Label(edit_task_frame, text="Task Desc.: ", bg="#ffe8b8")
    edit_taskdesc_label.grid(row=1, column=0, pady=(10, 0), ipadx=20)

    edit_duedate_textbox = Entry(edit_task_frame, width=30)
    edit_duedate_textbox.grid(row=2, column=1, padx=20, pady=(10, 0))
    edit_duedate_label = Label(edit_task_frame, text="Due Date: ", bg="#ffe8b8")
    edit_duedate_label.grid(row=2, column=0, pady=(10, 0), ipadx=20)

    edit_categoryid_textbox = Entry(edit_task_frame, width=30)
    edit_categoryid_textbox.grid(row=3, column=1, padx=20, pady=(10, 0))
    edit_categoryid_label = Label(edit_task_frame, text="Category ID: ", bg="#ffe8b8")
    edit_categoryid_label.grid(row=3, column=0, pady=(10, 5))

    edit_taskdone_textbox = Entry(edit_task_frame, width=30)
    edit_taskdone_textbox.grid(row=4, column=1, padx=20, pady=(10, 0))
    edit_taskdone_label = Label(edit_task_frame, text="Task Done: ", bg="#ffe8b8")
    edit_taskdone_label.grid(row=4, column=0, pady=(10, 5))

    # Submit button
    submit_task_edit_button = Button(edit_task_frame, text="Submit Edit", command=lambda:edit_task())
    submit_task_edit_button.grid(row=5, column=0, columnspan=2, pady=5, padx=10, ipadx=101)

    mariadb = db.cursor()

    
    mariadb.execute("USE `task-listing`")
    mariadb.execute("SELECT * FROM task WHERE taskid = " + edit_task_id)

    records = mariadb.fetchall()

    def get_str(string):
        if(string == '1'):
            return 'Yes'
        elif(string == '0'):
            return 'No'

    for record in records:
        edit_taskname_textbox.insert(0,record[2])
        edit_taskdesc_textbox.insert(0,record[3])
        edit_duedate_textbox.insert(0,record[5])
        edit_taskdone_textbox.insert(0,get_str(str(record[1])))
        edit_categoryid_textbox.insert(0,record[6])

    mariadb.close()

# submits category details
def submit_category():
    global db

    if(len(categoryname_textbox.get()) == 0):
            alert('Category Name is Empty')
            return

    mariadb = db.cursor()

    mariadb.execute("USE `task-listing`;")
    mariadb.execute("""
        INSERT INTO `category` (`categoryname`,`categorydesc`)
        VALUES (%(categoryname)s,%(categorydesc)s)
    """,
    {
        'categoryname': categoryname_textbox.get(),
        'categorydesc': categorydesc_textbox.get()
    }
    )

    categoryname_textbox.delete(0,END)
    categorydesc_textbox.delete(0,END)

    db.commit()
    mariadb.close
    return_to_menu(category_window)

# deletes category
def delete_category():
    global db
    global categoryid_select_textbox

    delete_category_id = categoryid_select_textbox.get()

    if (len(delete_category_id) == 0):
        alert('Category ID is Empty')
        return

    mariadb = db.cursor()

    mariadb.execute('USE `task-listing`')

    mariadb.execute('UPDATE `task` SET categoryid = NULL WHERE categoryid = %(categoryid)s',
    {
        'categoryid': delete_category_id
    }
    )

    mariadb.execute('DELETE FROM `category` WHERE categoryid = %(categoryid)s',
    {
        'categoryid': delete_category_id
    }
    )

    db.commit()
    mariadb.close()

    categoryid_select_textbox.delete(0,END)
    return_to_menu(category_window)

# initializes category window and its functions
def category_function():
    global db
    global categoryname_textbox
    global categorydesc_textbox
    global categoryid_select_textbox
    global category_window

    main_menu_window.withdraw()

    category_window = Tk()
    category_window.title("NotesDB")
    category_window.configure(bg="#ffe8b8")
    category_window.resizable(False,False)

    category_frame = LabelFrame(category_window, text="Category Menu", bg="#ffe8b8")
    category_frame.pack()

    categoryname_textbox = Entry(category_frame, width=30)
    categoryname_textbox.grid(row=1, column=1, padx=20, pady=(10, 0))

    categoryname_label = Label(category_frame, text="Category: ", bg="#ffe8b8")
    categoryname_label.grid(row=1, column=0, pady=(10, 5))

    categorydesc_textbox = Entry(category_frame, width=30)
    categorydesc_textbox.grid(row=2, column=1, padx=20, pady=(10, 0))

    categorydesc_label = Label(category_frame, text="Description: ", bg="#ffe8b8")
    categorydesc_label.grid(row=2, column=0, pady=(10, 5))

    category_addbutton = Button(category_frame, text="Add Category", command=submit_category)
    category_addbutton.grid(row=3, column=0, columnspan=2, pady=5, padx=10, ipadx=87)

    category_viewbutton = Button(category_frame, text="View Categories", command=view_both)
    category_viewbutton.grid(row=4, column=0, columnspan=2, pady=5, padx=10, ipadx=82)

    categoryid_select_textbox = Entry(category_frame, width=30)
    categoryid_select_textbox.grid(row=5, column=1, pady=(5, 5))

    categoryid_selectlabel = Label(category_frame, text="Select ID: ", bg="#ffe8b8")
    categoryid_selectlabel.grid(row=5, column=0, ipadx=20, pady=(5, 5))

    category_editbutton = Button(category_frame, text="Edit Category", command=edit_category_function)
    category_editbutton.grid(row=6, column=0, columnspan=2, pady=5, padx=10, ipadx=89)

    category_deletebutton = Button(category_frame, text="Delete Category", command=delete_category)
    category_deletebutton.grid(row=7, column=0, columnspan=2, pady=5, padx=10, ipadx=82)

    category_task_addbutton = Button(category_frame, text="Add Task To A Category", command=add_task_to_category_function)
    category_task_addbutton.grid(row=8, column=0, columnspan=2, pady=5, padx=10, ipadx=61)

    category_returnbutton = Button(category_frame, text="Exit to Menu",command=lambda: return_to_menu(category_window))
    category_returnbutton.grid(row=9, column=0, columnspan=2, pady=5, padx=10, ipadx=90)

# submit category edits
def edit_category():
    global db
    global edit_category_window
    global edit_categoryname_textbox
    global edit_categorydesc_textbox
    global edit_category_id

    mariadb = db.cursor()

    mariadb.execute('USE `task-listing`')
    mariadb.execute("""
        UPDATE category SET
        `categoryname` = %(categoryname)s,
        `categorydesc` = %(categorydesc)s
        WHERE categoryid = %(categoryid)s
    """,
    {
        'categoryname': edit_categoryname_textbox.get(),
        'categorydesc': edit_categorydesc_textbox.get(),
        'categoryid': edit_category_id
    }
    )

    db.commit()
    mariadb.close()

    edit_categoryname_textbox.delete(0,END)
    edit_categorydesc_textbox.delete(0,END)

    edit_category_window.destroy()
    category_window.deiconify()

# initializes category editor window
def edit_category_function():
    global db
    global edit_category_window
    global edit_categoryname_textbox
    global edit_categorydesc_textbox
    global edit_category_id

    edit_category_id = categoryid_select_textbox.get()

    if (len(edit_category_id) == 0):
        alert('Category ID is Empty')
        return
    
    category_window.withdraw()

    edit_category_window = Tk()
    edit_category_window.title("NotesDB")
    edit_category_window.configure(bg="#ffe8b8")

    editcategory_frame = LabelFrame(edit_category_window, text="Edit Category", bg="#ffe8b8")
    editcategory_frame.pack(ipady=127)

    edit_categoryname_textbox = Entry(editcategory_frame, width=30)
    edit_categoryname_textbox.grid(row=0, column=1, padx=20, pady=(10, 0))

    edit_categoryname_label = Label(editcategory_frame, text="Category: ", bg="#ffe8b8")
    edit_categoryname_label.grid(row=0, column=0, pady=(10, 5))

    edit_categorydesc_textbox = Entry(editcategory_frame, width=30)
    edit_categorydesc_textbox.grid(row=1, column=1, padx=20, pady=(10, 0))

    edit_categorydesc_label = Label(editcategory_frame, text="Description: ", bg="#ffe8b8")
    edit_categorydesc_label.grid(row=1, column=0, pady=(10, 5))

    submit_category_edit_button = Button(editcategory_frame, text="Submit Edit", command=edit_category)
    submit_category_edit_button.grid(row=2, column=0, columnspan=2, pady=5, padx=10, ipadx=101)

    mariadb = db.cursor()

    mariadb.execute("USE `task-listing`")
    mariadb.execute("SELECT * FROM category WHERE categoryid = " + edit_category_id)

    categories = mariadb.fetchall()

    for category in categories:
        edit_categoryname_textbox.insert(0,category[1])
        edit_categorydesc_textbox.insert(0,category[2])

    mariadb.close()

# submits task to a category
def submit_task_to_category():
    global db
    global add_category_task_window
    global add_category_taskname_textbox
    global add_category_taskdesc_textbox
    global add_category_duedate_textbox
    global add_category_categoryid_textbox
    global add_category_taskdone_textbox

    def get_bool(string):
        eval_str = string
        if(eval_str.lower() == 'yes'):
            return '1'
        elif(eval_str.lower() == 'no'):
            return '0'

    bool_task = get_bool(add_category_taskdone_textbox.get())

    if(len(add_category_taskname_textbox.get()) == 0 or (bool_task != "1" or "0")):
            alert('Task Name or Task Progress is Empty')
            return

    mariadb = db.cursor()

    mariadb.execute("USE `task-listing`")
    mariadb.execute("""INSERT INTO `task` (taskname, taskdesc, adddate, duedate, isdone, categoryid)
    VALUES (%(taskname)s, %(taskdesc)s, CURDATE(), %(duedate)s, %(isdone)s, %(categoryid)s)""",
    {
        'taskname': add_category_taskname_textbox.get(),
        'taskdesc': add_category_taskdesc_textbox.get(),
        'duedate': add_category_duedate_textbox.get(),
        'isdone': bool_task,
        'categoryid': add_category_categoryid_textbox.get()
    }
    )

    db.commit()
    mariadb.close()

    add_category_taskname_textbox.delete(0,END)
    add_category_taskdesc_textbox.delete(0,END)
    add_category_duedate_textbox.delete(0,END)
    add_category_categoryid_textbox.delete(0,END)
    add_category_taskdone_textbox.delete(0,END)

    show_tasks(view_all_tasks_frame)
    return_to_menu(add_category_task_window)

# initializes window for adding task to a category
def add_task_to_category_function():
    global db
    global add_category_task_window
    global add_category_taskname_textbox
    global add_category_taskdesc_textbox
    global add_category_duedate_textbox
    global add_category_categoryid_textbox
    global add_category_taskdone_textbox
    global categoryid_select_textbox

    add_category_task_id = categoryid_select_textbox.get()

    if (len(add_category_task_id) == 0):
        alert('Category ID is Empty')
        return
        
    category_window.destroy()

    add_category_task_window = Tk()
    add_category_task_window.title("NotesDB")
    add_category_task_window.configure(bg="#ffe8b8")

    add_category_task_frame = LabelFrame(add_category_task_window, text="Add Task to a Category", bg="#ffe8b8")
    add_category_task_frame.pack(fill="both")

    add_category_taskname_textbox = Entry(add_category_task_frame, width=30)
    add_category_taskname_textbox.grid(row=0, column=1, padx=20, pady=(10, 0))
    add_category_taskname_label = Label(add_category_task_frame, text="Task Name: ", bg="#ffe8b8")
    add_category_taskname_label.grid(row=0, column=0, pady=(10, 0), ipadx=20)

    add_category_taskdesc_textbox = Entry(add_category_task_frame, width=30)
    add_category_taskdesc_textbox.grid(row=1, column=1, padx=20, pady=(10, 0))
    add_category_taskdesc_label = Label(add_category_task_frame, text="Task Desc.: ", bg="#ffe8b8")
    add_category_taskdesc_label.grid(row=1, column=0, pady=(10, 0), ipadx=20)

    add_category_duedate_textbox = Entry(add_category_task_frame, width=30)
    add_category_duedate_textbox.grid(row=2, column=1, padx=20, pady=(10, 0))
    add_category_duedate_textbox.insert(0,"yy-mm-dd")
    add_category_duedate_label = Label(add_category_task_frame, text="Due Date: ", bg="#ffe8b8")
    add_category_duedate_label.grid(row=2, column=0, pady=(10, 0), ipadx=20)

    add_category_categoryid_textbox = Entry(add_category_task_frame, width=30)
    add_category_categoryid_textbox.grid(row=3, column=1, padx=20, pady=(10, 0))
    add_category_categoryid_textbox.insert(0,add_category_task_id)
    add_category_categoryid_label = Label(add_category_task_frame, text="Category ID: ", bg="#ffe8b8")
    add_category_categoryid_label.grid(row=3, column=0, pady=(10, 5))

    add_category_taskdone_textbox = Entry(add_category_task_frame, width=30)
    add_category_taskdone_textbox.grid(row=4, column=1, padx=20, pady=(10, 0))
    add_category_taskdone_textbox.insert(0,"Yes/No")
    add_category_taskdone_label = Label(add_category_task_frame, text="Task Done: ", bg="#ffe8b8")
    add_category_taskdone_label.grid(row=4, column=0, pady=(10, 5))

    submit_category_task_button = Button(add_category_task_frame, text="Submit Edit", command=submit_task_to_category)
    submit_category_task_button.grid(row=5, column=0, columnspan=2, pady=5, padx=10, ipadx=101)

# alert function where you can input a message that will pop up
def alert(message, kind='info', hidemain=True):
    if kind not in ('error', 'warning', 'info'):
        raise ValueError('Unsupported alert kind.')
    
    show_method = getattr(messagebox, 'show{}'.format(kind))
    show_method('Error', message)

# fetches current tasks and displays them in a frame
def show_tasks(frame_var):
    global db
    mariadb = db.cursor()

    mariadb.execute("USE `task-listing`")
    mariadb.execute("SELECT taskid, taskname, taskdesc, duedate, isdone, categoryname FROM task t LEFT JOIN category c ON t.categoryid = c.categoryid;")
    
    records = mariadb.fetchall()

    print_records = 'ID | Task Done:\tCategory Name | Task Name: Description | Due on: Date'

    show_label = Label(frame_var, text=print_records, bg="#ffe8b8")
    show_label.grid(row=0, column=0, columnspan=2, sticky='w', padx=(0,10), pady=(0,10))

    print_records = ''

    def is_done(input):
        if(input=="1"):
            return "Finished"
        elif(input=="0"):
            return "On Going"

    counter = 1

    for record in records:
        print_records = (str(record[0]) + " | "
        + is_done(str(record[4])) + ": \t"
        + str(record[5]) + " | "
        + str(record[1]) + ": "
        + str(record[2]) + " | Due on: " 
        + str(record[3])
        )

        show_results = Label(frame_var, text=print_records, bg="#ffe8b8")
        show_results.grid(row=counter,column=0,columnspan=2,sticky='w',padx=(0,10))

        counter += 1

    mariadb.close()

# fetches categories and displays them in a frame
def show_categories(frame_var):
    global db
    mariadb = db.cursor()

    mariadb.execute('USE `task-listing`')
    mariadb.execute('SELECT * FROM category')

    categories = mariadb.fetchall()

    print_categories = 'ID | Category Name: Description'

    show_label = Label(frame_var, text=print_categories, bg="#ffe8b8")
    show_label.grid(row=0, column=0, columnspan=2, sticky='w', padx=(0,10), pady=(0,10))

    print_categories = ''

    counter = 1

    for category in categories:
        print_categories = (str(category[0]) + " | "
        + str(category[1]) + ": "
        + str(category[2])
        )   

        show_results = Label(frame_var, text=print_categories, bg="#ffe8b8")
        show_results.grid(row=counter,column=0,columnspan=2,sticky='w',padx=(0,10))

        counter += 1

    mariadb.close()

root.mainloop()