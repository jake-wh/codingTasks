from task_repo.task_repo import TaskRepository
from create_and_delete.create_and_delete import CreateAndDelete
from categorise.categorise import Categorise


class TaskManager:
    '''
    Class which houses methods that performs all the operations that the
    application will use.
    '''
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository
        self.create_and_delete = CreateAndDelete(self.task_repository)
        self.categorise = Categorise(self.task_repository)

    def new_task(self, *args: str) -> None:
        '''
        Create a new task within the task repository.

        Parameters (all type `str`):\n
        Task name (mandatory); Task description (mandatory);
        Task folder (optional); Priority tag (optional)
        '''
        self.create_and_delete.create_task(*args)

    def remove_task(self, *args: int) -> None:
        '''
        Delete one or multiple tasks from the task repository.
        If multiple `task_id`s are entered, the must be separated by commas.

        Parameter(s):
        `task_id`: `int`
        '''
        self.create_and_delete.delete_task(*args)

    def view_tasks(self, task_id: int = None) -> list:
        '''
        Lists all tasks in the repository, showing incomplete tasks before
        completed tasks. Or if a `task_id` is provided, return the specified
        task.

        Parameters:
        (Optional) `task_id`: `int`
        '''
        self.task_repository.list_tasks(task_id)

    def view_tick(self, completed: bool):
        '''
        List all tasks that are either complete or incomplete.
        '''
        self.task_repository.list_todo_or_completed(completed)

    def edit_task(self, task_id: int, new_name: str,
                    new_description: str):
        '''
        Update a task in the repository's name and description.
        '''
        self.task_repository.update_task(task_id, new_name, new_description)

    def search_folder(self, task_folder: str = None):
        '''
        Search the repository for tasks that are assigned to a
        specific task folder.
        '''
        self.task_repository.list_folder(task_folder)

    def add_or_change_task_folder(self, *args) -> None:
        '''
        Updates the `task_folder` property of a task in the repository.

        When both `task_id` and `task_folder` are provided, it will update
        the `task_folder` to the new value given for the specified `task_id`.
        If only one argument is entered, it will clear the `task_folder`
        value for the specified `task_id`.

        Parameters:\n
        (Mandatory) `task_id`: `int`\n
        (Optional) `task_folder`: `str`
        '''
        self.categorise.update_folder(*args)

    def delete_folder_or_folders(self, *args) -> None:
        '''
        Deletes all tasks from specified task folders. If multiple arguments
        are given, they must be separated by commas.

        Parameters:\n
        `task_folder`: `str`
        '''
        self.create_and_delete.delete_all_from_folder(*args)

    def delete_folder(self, *args: str):
        '''
        Deletes all tasks from specified folder.
        '''
        self.create_and_delete.delete_all_from_folder(*args)

    def assign_priority(self, *args) -> None:
        '''
        Updates the `priority_tag` property of a task in the repository.

        When both `task_id` and `priority_tag` are provided, it will update
        the `priority_tag` to the new value given for the specified `task_id`.
        If only one argument is entered, it will clear the `priority_tag`
        value for the specified `task_id`.

        Parameters:\n
        (Mandatory) `task_id`: `int`\n
        (Optional) `priority_tag`: `str`
        '''
        self.categorise.update_priority(*args)

    def tick_task(self, task_id: int) -> None:
        '''
        Toggles a Task complete or incomplete.
        '''
        self.task_repository.toggle_completed(task_id)
