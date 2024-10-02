import sqlite3
import unittest
from datetime import date
from src.task_repo.task_repo import TaskRepository
from src.task.task import Task


class TestTaskRepository(unittest.TestCase):

    def setUp(self):
        self.test_conn = sqlite3.connect(":memory:")
        self.test_repo = TaskRepository(self.test_conn)
        self.test_repo.initialise_database()
        self.current_date = date.today().isoformat()

    def tearDown(self):
        self.test_conn.close()

    def test_list_tasks_with_one_task(self):
        add_tasks = """INSERT INTO Task_Repository (name, description)
        VALUES (?, ?)"""
        self.test_repo.cursor.execute(add_tasks, ("test", "test description"))
        self.test_conn.commit()
        result = [
            Task(1, False, 'test', 'test description',
                 self.current_date, None, None)
            ]
        test = self.test_repo.list_tasks()
        self.assertEqual(result, test)

    def test_list_tasks_with_multiple_tasks(self):
        '''
        Testing to see if the incomplete tasks are displayed before
        completed tasks.
        '''
        add_tasks = """INSERT INTO Task_Repository (name, description)
        VALUES (?, ?)"""
        self.test_repo.cursor.execute(add_tasks, ("test", "test description"))

        add_tasks2 = """INSERT INTO Task_Repository (name, description,
        completed) VALUES (?, ?, ?)"""
        self.test_repo.cursor.execute(add_tasks2, ("test2",
                                                   "test description2", 1))

        add_tasks3 = """INSERT INTO Task_Repository (name, description)
        VALUES (?, ?)"""
        self.test_repo.cursor.execute(add_tasks3, ("test3",
                                                   "test description3"))
        self.test_conn.commit()

        result = [
            Task(1, False, 'test', 'test description',
                 self.current_date, None, None),
            Task(3, False, 'test3', 'test description3',
                 self.current_date, None, None),
            Task(2, True, 'test2', 'test description2',
                 self.current_date, None, None)
            ]
        test = self.test_repo.list_tasks()
        self.assertEqual(result, test)

    def test_list_tasks_with_specified_task_id(self):
        add_tasks = """INSERT INTO Task_Repository (name, description)
        VALUES (?, ?)"""
        self.test_repo.cursor.execute(add_tasks, ("test", "test description"))
        add_tasks2 = """INSERT INTO Task_Repository (name, description,
        completed) VALUES (?, ?, ?)"""
        self.test_repo.cursor.execute(add_tasks2, ("test2",
                                                   "test description2", 1))
        add_tasks3 = """INSERT INTO Task_Repository (name, description)
        VALUES (?, ?)"""
        self.test_repo.cursor.execute(add_tasks3, ("test3",
                                                   "test description3"))
        self.test_conn.commit()
        result = [
            Task(3, False, 'test3', 'test description3',
                 self.current_date, None, None)
            ]
        test = self.test_repo.list_tasks(3)
        self.assertEqual(result, test)

    def test_list_tasks_with_no_tasks(self):
        result = []
        test = self.test_repo.list_tasks()
        self.assertEqual(result, test)

    def test_list_todo_or_completed_as_todo(self):
        add_tasks = """INSERT INTO Task_Repository (name, description)
        VALUES (?, ?)"""
        self.test_repo.cursor.execute(add_tasks, ("test", "test description"))

        add_tasks2 = """INSERT INTO Task_Repository (name, description,
        completed) VALUES (?, ?, ?)"""
        self.test_repo.cursor.execute(add_tasks2, ("test2",
                                                   "test description2", 1))
        add_tasks3 = """INSERT INTO Task_Repository (name, description)
        VALUES (?, ?)"""
        self.test_repo.cursor.execute(add_tasks3, ("test3",
                                                   "test description3"))
        self.test_conn.commit()

        result = [
            Task(1, False, 'test', 'test description',
                 self.current_date, None, None),
            Task(3, False, 'test3', 'test description3',
                 self.current_date, None, None)
            ]
        test = self.test_repo.list_todo_or_completed(False)
        self.assertEqual(result, test)

    def test_list_todo_or_completed_as_completed(self):
        add_tasks = """INSERT INTO Task_Repository (name, description)
        VALUES (?, ?)"""
        self.test_repo.cursor.execute(add_tasks, ("test", "test description"))

        add_tasks2 = """INSERT INTO Task_Repository (name, description,
        completed) VALUES (?, ?, ?)"""
        self.test_repo.cursor.execute(add_tasks2, ("test2",
                                                   "test description2", True))

        add_tasks3 = """INSERT INTO Task_Repository (name, description)
        VALUES (?, ?)"""
        self.test_repo.cursor.execute(add_tasks3, ("test3",
                                                   "test description3"))
        self.test_conn.commit()

        result = [
            Task(2, True, 'test2', 'test description2',
                 self.current_date, None, None)
            ]
        test = self.test_repo.list_todo_or_completed(1)
        self.assertEqual(result, test)

    def test_list_todo_or_completed_as_todo_with_no_tasks(self):
        result = []
        test = self.test_repo.list_todo_or_completed(0)
        self.assertEqual(result, test)

    def test_list_todo_or_completed_as_completed_with_no_tasks(self):
        result = []
        test = self.test_repo.list_todo_or_completed(1)
        self.assertEqual(result, test)

    def test_list_folder(self):
        add_tasks = """INSERT INTO Task_Repository (name, description,
        task_folder) VALUES (?, ?, ?)"""
        self.test_repo.cursor.execute(add_tasks, ("test", "test description",
                                                    "Project 1"))

        add_tasks2 = """INSERT INTO Task_Repository (name, description,
        completed, task_folder) VALUES (?, ?, ?, ?)"""
        self.test_repo.cursor.execute(add_tasks2, ("test2", "test description2",
                                                    "1", "Project 1"))

        add_tasks3 = """INSERT INTO Task_Repository (name, description)
        VALUES (?, ?)"""
        self.test_repo.cursor.execute(add_tasks3, ("test3",
                                                   "test description3"))
        self.test_conn.commit()

        result = [
            Task(1, False, 'test', 'test description', self.current_date,
                 'Project 1', None),
            Task(2, True, 'test2', 'test description2', self.current_date,
                 'Project 1', None)
            ]
        test = self.test_repo.list_folder('Project 1')
        self.assertEqual(result, test)

    def test_list_folder_when_no_args_given(self):
        add_tasks = """INSERT INTO Task_Repository (name, description,
        task_folder) VALUES (?, ?, ?)"""
        self.test_repo.cursor.execute(add_tasks, ("test", "test description",
                                                    "Project 1"))

        add_tasks2 = """INSERT INTO Task_Repository (name, description,
        task_folder) VALUES (?, ?, ?)"""
        self.test_repo.cursor.execute(add_tasks2, ("test2",
                                            "test description2", "Project 1"))

        add_tasks3 = """INSERT INTO Task_Repository (name, description,
        task_folder, completed) VALUES (?, ?, ?, ?)"""
        self.test_repo.cursor.execute(add_tasks3, ("test3",
                                        "test description3", "Project 2", "1"))

        add_tasks4 = """INSERT INTO Task_Repository (name, description,
        task_folder) VALUES (?, ?, ?)"""
        self.test_repo.cursor.execute(add_tasks4, ("test4",
                                            "test description4", "Project 2"))

        add_tasks5 = """INSERT INTO Task_Repository (name, description,
        task_folder) VALUES (?, ?, ?)"""
        self.test_repo.cursor.execute(add_tasks5, ("test5",
                                            "test description5", "Project 3"))
        self.test_conn.commit()

        result = [
            Task(1, False, 'test', 'test description', self.current_date,
                 'Project 1', None),
            Task(2, False, 'test2', 'test description2', self.current_date,
                 'Project 1', None),
            Task(4, False, 'test4', 'test description4', self.current_date,
                 'Project 2', None),
            Task(5, False, 'test5', 'test description5', self.current_date,
                 'Project 3', None),
            Task(3, True, 'test3', 'test description3', self.current_date,
                 'Project 2', None)
            ]
        test = self.test_repo.list_folder()
        self.assertEqual(result, test)

    def test_list_folder_when_no_tasks_are_in_list_folder(self):
        add_tasks = """INSERT INTO Task_Repository (name, description)
        VALUES (?, ?)"""
        self.test_repo.cursor.execute(add_tasks, ("test", "test description"))
        self.test_conn.commit()
        result = []
        test = self.test_repo.list_folder("Project 1")
        self.assertEqual(result, test)

    def test_list_folder_when_incorrect_task_folder_given(self):
        add_tasks = """INSERT INTO Task_Repository (name, description,
        task_folder) VALUES (?, ?, ?)"""
        self.test_repo.cursor.execute(add_tasks, ("test", "test description",
                                                    "Project 1"))
        self.test_conn.commit()
        result = []
        test = self.test_repo.list_folder("fake project")
        self.assertEqual(result, test)

    def test_update_task(self):
        add_tasks = """INSERT INTO Task_Repository (name, description)
        VALUES (?, ?)"""
        self.test_repo.cursor.execute(add_tasks, ("test", "test description"))
        self.test_conn.commit()
        result = [
            Task(1, False, 'updated_task', 'updated_description',
                       self.current_date, None, None)
            ]
        self.test_repo.update_task(1, "updated_task", "updated_description")
        test = self.test_repo.list_tasks()
        self.assertEqual(result, test)

    def test_update_task_when_task_id_does_not_exist(self):
        result = None
        test = self.test_repo.update_task(1, "updated_task",
                                           "updated_description")
        self.assertEqual(result, test)

    def test_toggle_completed(self):
        add_task = """INSERT INTO Task_Repository (name, description)
        VALUES (?, ?)"""
        self.test_repo.cursor.execute(add_task, ("test", "test description"))
        result = [
            Task(1, True, 'test', 'test description',
                 self.current_date, None, None)
        ]
        self.test_repo.toggle_completed(1)
        test = self.test_repo.list_tasks()
        self.assertEqual(result, test)

    def test_toggle_completed_when_task_does_not_exist(self):
        add_task = """INSERT INTO Task_Repository (name, description)
        VALUES (?, ?)"""
        self.test_repo.cursor.execute(add_task, ("test", "test description"))
        result = [
            Task(1, False, 'test', 'test description',
                 self.current_date, None, None)
        ]
        self.test_repo.toggle_completed(3)
        test = self.test_repo.list_tasks()
        self.assertEqual(result, test)


if __name__ == "__main__":
    unittest.main()
