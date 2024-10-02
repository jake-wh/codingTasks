class Task:
    def __init__(self, task_id=None, completed=0, name='', description='',
                 date_added=None, task_folder=None, priority_tag=None):
        '''
        Task object initiator class. All attributes are empty by default, to
        be added either manually or automatically when the object is queried
        into the database.
        '''
        self.task_id = task_id
        self.completed = completed
        self.name = name
        self.description = description
        self.date_added = date_added
        self.task_folder = task_folder
        self.priority_tag = priority_tag

    def __eq__(self, other):
        '''
        This function allows comparing tasks based on their attributes
        rather than their storage space in memory, allowing efficient
        testing.
        '''
        return (
            self.task_id == other.task_id and
            self.completed == other.completed and
            self.name == other.name and
            self.description == other.description and
            self.date_added == other.date_added and
            self.task_folder == other.task_folder and
            self.priority_tag == other.priority_tag)

    def __repr__(self):
        '''
        This function allows Task object attributes to be printed instead
        of their storage space in memory.
        '''
        return f"Task({self.task_id}, {self.completed}, \
            {self.name}, {self.description}, {self.date_added}, \
                {self.task_folder}, {self.priority_tag})"

    def __str__(self):
        return (f"ID: {self.task_id} / COMP: {self.completed} / "
                f"NAME: {self.name} / DESC: {self.description} / "
                f"DATE: {self.date_added} / FOLD: {self.task_folder} / "
                f"PRIO: {self.priority_tag}")
