from task_manager.task_manager import TaskManager
from task_repo.task_repo import TaskRepository
# ----------------------------------------
### Functions ###


def handle_view_tasks(task_manager):
    print("""\n-> "View Tasks"

Please choose:
1. Tasks
2. Incomplete Tasks
3. Completed Tasks
4. Main menu""")
    view_menu = input("\nEnter here: ")

    if view_menu == '1':
        print("""\nView a task by entering the task ID, or enter 'n'
to view all.

Or, type 'back' to return to the main menu.""")
        view = input("Enter here: ")

        if view == 'n':
            print("\n-> All Tasks:")
            print("""\nTask Key:
ID, Comp/Incomp, Name, Description, Date, Folder, Priority\n""")
            task_manager.view_tasks()
            print("*")
        elif view.lower() == 'back':
            return
        else:
            print("\n-> Select Task:")
            print("""\nTask Key:
ID, Comp/Incomp, Name, Description, Date, Folder, Priority\n""")
            task_manager.view_tasks(view)
            print("*")

    elif view_menu == '2':
        print("\n-> Incomplete Tasks:")
        print("""\nTask Key:
ID, Comp/Incomp, Name, Description, Date, Folder, Priority\n""")
        task_manager.view_tick(False)
        print("*")

    elif view_menu == '3':
        print("\n-> Completed Tasks:")
        print("""\nTask Key:
ID, Comp/Incomp, Name, Description, Date, Folder, Priority\n""")
        task_manager.view_tick(True)
        print("*")

    elif view_menu == '4':
        return


def handle_create_task(task_manager):

    print("""\n-> "Create a Task"

Requires the Name and Description of the Task.
It can also optionally be assigned to a Task Folder,
and can also be assigned a Priority Tag.

To not specify a Task Folder or Priority tag, Enter with no value.\n""")

    name = input("Task Name: ")
    description = input("Task Description: ")
    folder = input("Task Folder: ")
    priority = input("Task Priority: ")

    if folder == "" and priority == "":
        task_manager.new_task(name, description)
    elif priority == "":
        task_manager.new_task(name, description, folder)
    else:
        task_manager.new_task(name, description, folder, priority)
    print("*")


def handle_edit_task(task_manager):

    print("""\n-> Edit Task

1. Edit Name and Description
2. Update Folder for Task
3. Update Priority for Task
4. Mark Complete/Incomplete
""")
    choice = input("\nEnter here: ")

    if choice == '1':

        print("""\n-> Edit Name and Description

Enter the Task ID of the task you would like to update,
then enter the new Name and Description for the task.\n""")

        edit_id = int(input("Enter the Task ID you would like to "
"edit: "))
        edit_name = input("Enter the new Name: ")
        edit_desc = input("Enter the new Description: ")
        task_manager.edit_task(edit_id, edit_name, edit_desc)
        print("Task updated successfully!")
        print("*")

    elif choice == '2':

        print("""\n-> Update Folder for Task

Enter the Task ID of the task you would like to update,
then enter the new Task Folder name for the task.

If you would like to unassign a Folder for a Task,
Enter the Task ID and give no value for Task Folder\n""")

        edit_id = input("Enter the Task ID you would like to "
"edit: ")
        edit_folder = input("Enter the desired updated Folder name "
                            "(leave empty to unassign folder): ")
        if edit_folder == "":
            task_manager.add_or_change_task_folder(int(edit_id))
        else:
            task_manager.add_or_change_task_folder(int(edit_id), edit_folder)
        print("\nFolder for Task successfully updated!")
        print("*")

    elif choice == '3':

        print("""\n-> Update Priority for Task

Enter the Task ID of the task you would like to update,
then enter the Priority Tag you would like to assign.

If you would like to unassign Priority for a Task,
Enter the Task ID and give no value for Priority.\n""")

        edit_id = int(input("Enter the Task ID you would like to "
"edit: "))
        edit_priority = input("Enter the desired updated Priority Tag "
                            "(leave empty to unassign): ")
        if edit_priority == "":
            task_manager.assign_priority(edit_id)
        else:
            task_manager.assign_priority(edit_id, edit_priority)
        print("Folder for Task successfully updated!")
        print("*")

    elif choice == '4':

        print("""\n-> Mark Complete/Incomplete

Toggle a Task as Complete or Incomplete.""")
        id = int(input("Enter a Task ID: "))
        task_manager.tick_task(id)

    elif choice == '5':
        return


def handle_delete_task(task_manager):

    print("""\n-> Delete Task

Delete a Task from the Repository by entering its ID.
Stop deleting Tasks by entering n.""")

    select = input("Enter a Task ID to delete: ")
    task_manager.remove_task(int(select))
    print("Task(s) successfully deleted!")
    print("*")


def handle_view_task_folders(task_manager):

    print("""\n-> View Task folder(s)

List all tasks from a specified Task Folder.
Enter no value to list all Tasks that have been assigned to a Folder.""")

    folder = input("Enter a folder name: ")
    print()
    if folder:
        task_manager.search_folder(folder)
    elif folder == "":
        task_manager.search_folder()
    print("*")


def handle_delete_task_folder(task_manager):

    print("""\n-> Delete Task folder

Deletes all tasks from a specified Task Folder.""")

    select = input("Enter a Task Folder to delete, or n to go back: ")
    if select:
        task_manager.delete_folder(select)
    elif select == 'n':
        return

    print("\nFolder successfully deleted!")
    print("*")


# ----------------------------------------
### Program Start ###


def main():

    task_manager = TaskManager(TaskRepository())

    menu = True

    print("\nWelcome to the Task Manager!")

    while menu:
        print("""\nMain Menu:

1. View Tasks
2. Create Task
3. Edit Task
4. Delete Task
5. View Task Folder
6. Delete Task Folder
7. Exit App

Choose your option by entering the corresponding number.""")
        choice = input("Enter here: ")

        if choice == '1':
            handle_view_tasks(task_manager)

        elif choice == '2':
            handle_create_task(task_manager)

        elif choice == '3':
            handle_edit_task(task_manager)

        elif choice == '4':
            handle_delete_task(task_manager)

        elif choice == '5':
            handle_view_task_folders(task_manager)

        elif choice == '6':
            handle_delete_task_folder(task_manager)

        elif choice == '7':
            print("\nExiting App. Goodbye!")
            menu = False
            task_manager.task_repository.conn.close()


if __name__ == "__main__":
    main()

# Apologies for the late upload of this task.
# There are some functionalities I am going to improve soon,
# but I feel comfortable uploading this for now.

# Please note that when the venv interpreter is selected,
# the program runs but the testing tab on the left bar cannot
# then find the tests. However, when I add src to the start of all the
# relative import paths
# (e.g. from src.categorise.categorise import Categorise),
# the testing suite can then find them but when running
# the program it crashes because 'no module names 'src''.

# When changing to the global interpreter however, adding src. to
# the relative paths allows both the tests to appear in the testing tab
# and also allows the program to run. I was stuck on this for hours,
# any advice on why this is happening would be greatly appreciated.
