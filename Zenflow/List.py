import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3 as sql

guiWindow=None
def list():
    global guiWindow
    if guiWindow and guiWindow.winfo_exists():
        guiWindow.destroy()
        guiWindow=None
        return
    def add_task():
        task_string = task_field.get()
        if len(task_string) == 0:
            messagebox.showinfo('Error', 'Field is Empty.')
        else:
            tasks.append(task_string)
            the_cursor.execute('insert into tasks values (?)', (task_string,))
            the_connection.commit()
            list_update()
            task_field.delete(0, 'end')

    def list_update():
        clear_list()
        for task in tasks:
            task_listbox.insert('end', task)

    def delete_task():
        try:
            the_value = task_listbox.get(task_listbox.curselection())
            if the_value in tasks:
                tasks.remove(the_value)
                list_update()
                the_cursor.execute('delete from tasks where title = ?', (the_value,))
                the_connection.commit()
        except:
            messagebox.showinfo('Error', 'No Task Selected. Cannot Delete.')

    def delete_all_tasks():
        message_box = messagebox.askyesno('Delete All', 'Are you sure?')
        if message_box == True:
            while(len(tasks) != 0):
                tasks.pop()
            the_cursor.execute('delete from tasks')
            the_connection.commit()
            list_update()

    def clear_list():
        task_listbox.delete(0, 'end')

    def close():
        print(tasks)
        the_connection.commit()
        the_cursor.close()
        guiWindow.destroy()


    def retrieve_database():
        while(len(tasks) != 0):
            tasks.pop()
        for row in the_cursor.execute('select title from tasks'):
            tasks.append(row[0])

   
    guiWindow = tk.Toplevel()
    guiWindow.title("Check-List Manager")
    guiWindow.geometry("400x350+950+370")
    guiWindow.wm_overrideredirect(True)
    guiWindow.resizable(0, 0)
    guiWindow.configure(bg = "#BF3EFF")
    
   
    the_connection = sql.connect('listOfTasks.db')
    the_cursor = the_connection.cursor()
    the_cursor.execute('create table if not exists tasks (title text)')

    tasks = []

   
    header_frame = tk.Frame(guiWindow, bg = "#8A2BE2")
    functions_frame = tk.Frame(guiWindow, bg = "#8A2BE2")
    listbox_frame = tk.Frame(guiWindow, bg = "#8A2BE2")

    header_frame.pack(fill = "both")
    functions_frame.pack(side = "left", expand = True, fill = "both")
    listbox_frame.pack(side = "right", expand = True, fill = "both")

   
    header_label = ttk.Label(
        header_frame,
        text = "Check-List",
        font = ("Brush Script MT", "30"),
        background = "#8A2BE2",
        foreground = "#97FFFF"
    )
    header_label.pack(padx = 20, pady = 10)

    task_label = ttk.Label(
        functions_frame,
        text = "Enter the Task:",
        font = ("Consolas", "11", "bold"),
        background = "#8A2BE2",
        foreground = "#000000"
    )
    task_label.place(x = 20, y = 20)

    task_field = ttk.Entry(
        functions_frame,
        font = ("Consolas", "11"),
        width = 18,
        background = "#FFF8DC",
        foreground = "#A52A2A"
    )
    task_field.place(x = 20, y = 50)

  
    add_button = ttk.Button(
        functions_frame,
        text = "Add Task",
        width = 20,
        command = add_task
    )
    del_button = ttk.Button(
        functions_frame,
        text = "Delete Task",
        width = 20,
        command = delete_task
    )
    del_all_button = ttk.Button(
        functions_frame,
        text = "Delete All Tasks",
        width = 20,
        command = delete_all_tasks
    )
    exit_button = ttk.Button(
        functions_frame,
        text = "Exit",
        width = 20,
        command = close
    )
    add_button.place(x = 20, y = 90)
    del_button.place(x = 20, y = 130)
    del_all_button.place(x = 20, y = 170)
    exit_button.place(x = 20, y = 210)

   
    task_listbox = tk.Listbox(
        listbox_frame,
        width = 22,
        height = 10,
        selectmode = 'SINGLE',
        background = "#FFFFFF",
        foreground = "#000000",
        selectbackground = "#CD853F",
        selectforeground = "#FFFFFF"
    )
    task_listbox.place(x = 20, y = 50)

   
    retrieve_database()
    list_update()
    guiWindow.lift()
    guiWindow.attributes('-topmost', True)
    
if __name__ == "__main__":
    list()