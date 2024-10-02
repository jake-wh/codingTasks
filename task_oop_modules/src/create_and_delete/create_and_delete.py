from task_repo.task_repo import TaskRepository


class CreateAndDelete:
    '''
    Class to house logic for all task creation/deletion from task repository.
    '''
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def create_task(self, *args: str) -> None:
        '''
        Logic for creating tasks.
        Takes 2 to 4 `str` arguments in the following order: `name`,
        `description`, `task_folder` and `priority_tag`.
        '''
        # Two to four string arguments must be given
        if len(args) < 2:
            raise ValueError("Name and Description string arguments are "
                             "required.")
        if len(args) > 4:
            raise ValueError("The maximum number of arguments is four.")

        # Assign `name` and `description` to the first two arguments given
        name, description = args[0], args[1]

        # Check task with given name doesn't already exist
        self.task_repository.cursor.execute("""SELECT * FROM
        Task_Repository WHERE name = (?)""", (name,))
        name_check = self.task_repository.cursor.fetchone()
        if name_check:
            raise ValueError("Task with this name already exists.")

        # Check the arguments entered are strings
        if not isinstance(name, str) or not isinstance(description, str):
            raise ValueError("Arguments must be strings.")

        # In order, check the amount of arguments given is 3 and assign
        # the 3rd argument to `task_folder`, then check the amount of
        # arguments given is 4 and assign the 4th to `priority_tag`.
        task_folder = args[2] if len(args) > 2 else None
        priority_tag = args[3] if len(args) > 3 else None

        # Append the `task_folder` and `priority_tag` query tags and
        # function arguments to the respective lists
        attributes = ["name", "description"]
        values = [name, description]
        if task_folder is not None:
            attributes.append("task_folder")
            values.append(task_folder)
        if priority_tag is not None:
            attributes.append("priority_tag")
            values.append(priority_tag)

        # Create the query which will be entered into the database
        query_str = ', '.join(attributes)
        ques_mark_num = ', '.join(['?'] * len(values))
        query = f"""INSERT INTO Task_Repository ({query_str})
        VALUES ({ques_mark_num})"""
        self.task_repository.cursor.execute(query, values)
        self.task_repository.conn.commit()

        # Fetch `task_id` to confirm successful creation
        self.task_repository.cursor.execute("""SELECT * FROM Task_Repository
        WHERE name = (?)""", (name,))
        data = self.task_repository.cursor.fetchone()
        task_id = data[0]
        print(f"Task ({task_id}) successfully created.")

    def delete_task(self, *args: int) -> None:
        '''
        Logic for deleting tasks.
        Deletes tasks with the given `task_id: int`. Can take a single argument,
        or multiple separated by commas.
        '''
        # At least one argument must be given
        if len(args) == 0:
            raise ValueError("Please enter at least one Task ID.")

        # Delete for every `task_id` given
        for task_id in args:
            if not isinstance(task_id, int):
                raise TypeError("Task IDs must be integers.")

            query = "SELECT * FROM Task_Repository WHERE task_id = ?"
            self.task_repository.cursor.execute(query, (task_id,))
            data = self.task_repository.cursor.fetchone()
            if data:
                delete = "DELETE FROM Task_Repository WHERE task_id = ?"
                self.task_repository.cursor.execute(delete, (task_id,))
                self.task_repository.conn.commit()
                print(f"Task ({task_id}) successfully deleted.")
            else:
                raise ValueError(f"Task ({task_id}) not found.")

    def delete_all_from_folder(self, *args: str) -> None:
        '''
        Logic for deleting all tasks from a specified `task_folder: str`.\n
        Multiple `task_folder`s can be specified, separated by commas.
        '''
        # If no task_folder is specified, a TypeError will be raised
        if len(args) == 0:
            raise TypeError("Please enter a Task folder name.")

        for task_folder in args:

            # Argument passed for task folder must be a string
            if not isinstance(task_folder, str):
                raise TypeError("The Task folder name must be a string.")

            query = "SELECT * FROM Task_Repository WHERE task_folder = ?"
            self.task_repository.cursor.execute(query, (task_folder,))
            data = self.task_repository.cursor.fetchall()
            if data:
                delete = "DELETE FROM Task_Repository WHERE task_folder = ?"
                self.task_repository.cursor.execute(delete, (task_folder,))
                self.task_repository.conn.commit()
            else:
                raise ValueError("Task folder not found.")
