from task_repo.task_repo import TaskRepository


class Categorise:
    '''
    Initiate the Categorise class with TaskRepository.
    '''
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def update_folder(self, *args):
        '''
        Logic to update the `task_folder` for specified `task_id`.
        First selects the record from the database with the `task_id`
        to ensure it exists, then updates the `task_folder` for the
        desired task.

        If only one argument is entered, it will clear the `task_folder`
        name for the specified `task_id`.
        '''
        if len(args) == 0:
            raise ValueError("Please enter a valid Task ID.")
        if len(args) > 2:
            raise ValueError("Too many arguments given. Maximum: 2")

        # `task_id` is stored
        task_id = args[0]

        # Type check `task_id`
        if not isinstance(task_id, int):
            raise TypeError("Please enter valid arguments. "
                            "Task ID (Mandatory): int; "
                            "Task folder (Optional): str")

        if len(args) == 2:
            # `task_folder` is stored
            task_folder = args[1]
            # Type check `task_folder`
            if not isinstance(task_folder, str):
                raise TypeError("Please enter valid arguments. "
                                "Task ID (Mandatory): int; "
                                "Task folder (Optional): str")
            # Searching database table with `task_id`
            query = """SELECT * FROM Task_Repository WHERE task_id = ?"""
            self.task_repository.cursor.execute(query, (task_id,))
            data = self.task_repository.cursor.fetchone()
            # If task exists, update
            if data:
                update = """UPDATE Task_Repository SET task_folder = ?
                WHERE task_id = ?"""
                self.task_repository.cursor.execute(update, (task_folder,
                                                             task_id))
                self.task_repository.conn.commit()
            else:
                raise ValueError(f"No Task found with Task ID ({task_id}).")

        # If one arg is given
        else:
            query = """SELECT * FROM Task_Repository WHERE task_id = ?"""
            self.task_repository.cursor.execute(query, (task_id,))
            data = self.task_repository.cursor.fetchone()
            # If task exists, clear folder name
            if data:
                update = """UPDATE Task_Repository SET task_folder = ?
                WHERE task_id = ?"""
                self.task_repository.cursor.execute(update, (None, task_id))
                self.task_repository.conn.commit()
            else:
                raise ValueError(f"No Task found with Task ID ({task_id}).")

    def update_priority(self, *args):
        '''
        Logic to update the `priority_tag` for specified `task_id`.
        First selects the record from the database with the `task_id`
        to ensure it exists, then updates the `priority_tag` for the
        desired task.

        If only one argument is entered, it will clear the `priority_tag`
        name for the specified `task_id`.
        '''
        if len(args) == 0:
            raise ValueError("Please enter a valid Task ID.")
        if len(args) > 2:
            raise ValueError("Too many arguments given. Maximum: 2")

        # `task_id` is stored
        task_id = args[0]

        # Type check `task_id`
        if not isinstance(task_id, int):
            raise TypeError("Please enter valid arguments. "
                            "Task ID (Mandatory): int; "
                            "Priority tag (Optional): str")

        if len(args) == 2:
            # `priority_tag` is stored
            priority_tag = args[1]
            # Type check `priority_tag`
            if not isinstance(priority_tag, str):
                raise TypeError("Please enter valid arguments. "
                                "Task ID (Mandatory): int; "
                                "Priority tag (Optional): str")
            # Searching database table with `task_id`
            query = """SELECT * FROM Task_Repository WHERE task_id = ?"""
            self.task_repository.cursor.execute(query, (task_id,))
            data = self.task_repository.cursor.fetchone()
            # If task exists, update
            if data:
                update = """UPDATE Task_Repository SET priority_tag = ?
                WHERE task_id = ?"""
                self.task_repository.cursor.execute(update, (priority_tag,
                                                             task_id))
                self.task_repository.conn.commit()
            else:
                raise ValueError(f"No Task found with Task ID ({task_id}).")

        # If one arg is given
        else:
            query = """SELECT * FROM Task_Repository WHERE task_id = ?"""
            self.task_repository.cursor.execute(query, (task_id,))
            data = self.task_repository.cursor.fetchone()
            # If task exists, clear `priority_tag`
            if data:
                update = """UPDATE Task_Repository SET priority_tag = ?
                WHERE task_id = ?"""
                self.task_repository.cursor.execute(update, (None, task_id))
                self.task_repository.conn.commit()
            else:
                raise ValueError(f"No Task found with Task ID ({task_id}).")
