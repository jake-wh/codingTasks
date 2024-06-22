import sqlite3
from task.task import Task


class TaskRepository:
    '''
    This class initiates a database ("task_repository.sqlite3")
    to store tasks, and contains methods to access and view the
    tasks and task folders stored in the database.

    'conn=None' is a parameter which allows for testing.
    '''
    def __init__(self, conn: str = None) -> None:
        if conn is None:
            self.conn = sqlite3.connect("task_repository.sqlite3")
        else:
            self.conn = conn
        self.cursor = self.conn.cursor()
        self.initialise_database()

    def initialise_database(self) -> None:
        '''
        Creates the table within the database to store the tasks.
        '''
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Task_Repository (
        task_id INTEGER PRIMARY KEY AUTOINCREMENT,
        completed BOOLEAN NOT NULL DEFAULT FALSE,
        name VARCHAR(100) NOT NULL,
        description TEXT NOT NULL,
        date_added DATE DEFAULT CURRENT_DATE NOT NULL,
        task_folder VARCHAR(100),
        priority_tag VARCHAR(100)
        )""")
        self.conn.commit()

    def list_get_logic(self, lst: list[tuple]) -> list:
        '''
        Logic function for `list_tasks()` method.
        '''
        new_lst = []
        for row in lst:
            new_lst.append(Task(row[0], row[1], row[2], row[3],
                                row[4], row[5], row[6]))
        return new_lst

    def list_tasks(self, task_id=None) -> list:
        """
        Logic for listing tasks in the task repository.

        This method lists all tasks in the repository, showing
        incomplete tasks before completed tasks.

        Or if a `task_id` is provided, return the specified task.
        """
        if task_id is not None:
            self.cursor.execute("""
            SELECT * FROM Task_Repository WHERE task_id = ?
            """, (task_id,))
            data = self.cursor.fetchone()
            task = Task(data[0], data[1], data[2], data[3],
                         data[4], data[5], data[6])
            print(task)
            return [task]
        else:
            task_list = []

            self.cursor.execute("""
            SELECT * FROM Task_Repository WHERE completed = 0
            """)
            incomplete_tasks = self.cursor.fetchall()
            task_list.extend(self.list_get_logic(incomplete_tasks))

            self.cursor.execute("""
            SELECT * FROM Task_Repository WHERE completed = 1
            """)
            completed_tasks = self.cursor.fetchall()
            task_list.extend(self.list_get_logic(completed_tasks))

            for task in task_list:
                print(task)
            return task_list

    def list_todo_or_completed(self, completed: bool) -> list:
        '''
        Lists either all incomplete or completed tasks in the
        repository, dependant on the boolean parameter entered:
        \ncompleted = True
        \nincomplete = False
        '''
        self.cursor.execute("""
        SELECT * FROM Task_Repository WHERE completed = ?
        ORDER BY priority_tag DESC""", (completed,),)
        data = self.cursor.fetchall()
        task_list = self.list_get_logic(data)
        for task in task_list:
            print(task)
        return task_list

    def list_folder(self, task_folder: str = None) -> list:
        '''
        Retrieves all the tasks from a specified `task_folder` -
        incomplete then completed, in that order.

        If no `task_folder` is specified, retrieve all tasks that have been
        assigned to a task folder.
        '''
        if task_folder:
            self.cursor.execute("""
            SELECT * FROM Task_Repository WHERE task_folder = ?""",
            (task_folder,))
        else:
            self.cursor.execute("""
            SELECT * FROM Task_Repository WHERE task_folder IS NOT NULL
            ORDER BY completed ASC""")
        data = self.cursor.fetchall()
        task_list = self.list_get_logic(data)
        for task in task_list:
            print(task)
        return task_list

    def update_task(self, task_id: int, new_name: str,
                    new_description: str) -> None:
        query = """SELECT * FROM Task_Repository WHERE task_id = ?"""
        self.cursor.execute(query, (task_id,))
        data = self.cursor.fetchone()
        if data:
            update = """UPDATE Task_Repository
            SET name = ?, description = ?
            WHERE task_id = ?"""
            self.cursor.execute(update, (new_name, new_description, task_id))
            self.conn.commit()
        else:
            print("Error: Task not found.")

    def toggle_completed(self, task_id: int) -> None:
        query = """SELECT * FROM Task_Repository WHERE task_id = ?"""
        self.cursor.execute(query, (task_id,))
        data = self.cursor.fetchone()
        if data:
            is_complete = (0, 1)
            update = """UPDATE Task_Repository
            SET completed = ?
            WHERE task_id = ?"""
            if data[1] == 0:
                self.cursor.execute(update, (is_complete[1], task_id))
                self.conn.commit()
            else:
                self.cursor.execute(update, (is_complete[0], task_id))
                self.conn.commit()
            return True
        else:
            print("Error: Task not found.")
            return False
