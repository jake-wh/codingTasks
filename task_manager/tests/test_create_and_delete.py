import sqlite3
import unittest
from datetime import date
from src.create_and_delete.create_and_delete import CreateAndDelete
from src.task_repo.task_repo import TaskRepository
from src.task_repo.task_repo import Task


class TestCreateAndDelete(unittest.TestCase):

    def setUp(self):
        self.test_conn = sqlite3.connect(":memory:")
        self.test_repo = TaskRepository(self.test_conn)
        self.test_repo.initialise_database()
        self.current_date = date.today().isoformat()
        self.cad = CreateAndDelete(self.test_repo)
        # Link the repository to the CaD instance
        self.cad.task_repository = self.test_repo

    def tearDown(self):
        self.test_conn.close()

    def test_create_task_with_two_args(self):
        self.cad.create_task("test1", "test1 description")
        test = [
            Task(1, False, 'test1', 'test1 description',
                 self.current_date, None, None)
            ]
        result = self.test_repo.list_tasks()
        self.assertEqual(result, test)

    def test_create_task_with_three_args(self):
        self.cad.create_task("test1", "test1 description", "test1 folder")
        test = [
            Task(1, False, 'test1', 'test1 description',
                 self.current_date, 'test1 folder', None)
            ]
        result = self.test_repo.list_tasks()
        self.assertEqual(result, test)

    def test_create_task_with_four_args(self):
        self.cad.create_task("test1", "test1 description",
                             "test1 folder", "test priority")
        test = [
            Task(1, False, 'test1', 'test1 description',
                 self.current_date, 'test1 folder', 'test priority')
            ]
        result = self.test_repo.list_tasks()
        self.assertEqual(result, test)

    def test_create_task_with_one_arg(self):
        with self.assertRaises(ValueError) as context:
            self.cad.create_task("task 1")
        self.assertEqual(str(context.exception),
                         "Name and Description string arguments are required.")

    def test_create_task_with_five_args(self):
        with self.assertRaises(ValueError) as context:
            self.cad.create_task("task 1", "description 1", "task_folder 1",
                                 "priority_tag 1", "extra argument")
        self.assertEqual(str(context.exception),
                         "The maximum number of arguments is four.")

    def test_create_task_with_incorrect_arg_types(self):
        with self.assertRaises(ValueError) as context:
            self.cad.create_task(1, 2)
        self.assertEqual(str(context.exception), "Arguments must be strings.")

    def test_create_task_with_no_args(self):
        with self.assertRaises(ValueError) as context:
            self.cad.create_task()
        self.assertEqual(str(context.exception),
                         "Name and Description string arguments are required.")

    def test_create_task_with_same_name(self):
        with self.assertRaises(ValueError) as context:
            self.cad.create_task("test1", "test1 description")
            self.cad.create_task("test1", "test1 description")
        self.assertEqual(str(context.exception),
                         "Task with this name already exists.")

    def test_delete_task(self):
        self.cad.create_task("test", "test description")
        result = None
        test = self.cad.delete_task(1)
        self.assertEqual(result, test)

    def test_delete_task_with_no_args_given(self):
        with self.assertRaises(ValueError) as context:
            self.cad.delete_task()
        self.assertEqual(str(context.exception),
                         "Please enter at least one Task ID.")

    def test_delete_task_with_two_args_given(self):
        '''
        Add three tasks, delete the first two and then check only the
        third task is recalled with test_repo.list_tasks().
        '''
        self.cad.create_task("test", "test description")
        self.cad.create_task("test2", "test2 description")
        self.cad.create_task("test3", "test3 description")
        self.cad.delete_task(1, 2)
        test = self.test_repo.list_tasks()
        result = [Task(3, False, 'test3', 'test3 description',
                        self.current_date, None, None)]
        self.assertEqual(result, test)

    def test_delete_task_with_multiple_args_given(self):
        self.cad.create_task("test", "test description")
        self.cad.create_task("test2", "test2 description")
        self.cad.create_task("test3", "test3 description")
        self.cad.create_task("test4", "test4 description")
        self.cad.create_task("test5", "test5 description")
        self.cad.delete_task(4, 1, 5, 2)
        test = self.test_repo.list_tasks()
        result = [Task(3, False, 'test3', 'test3 description',
                        self.current_date, None, None)]
        self.assertEqual(result, test)

    def test_delete_task_with_incorrect_arg_type(self):
        self.cad.create_task("test", "test description")
        self.cad.create_task("test2", "test2 description")
        self.cad.create_task("test3", "test3 description")
        self.cad.create_task("test4", "test4 description")
        self.cad.create_task("test5", "test5 description")
        with self.assertRaises(TypeError) as context:
            self.cad.delete_task(2, 3, 'four', 5)
        self.assertEqual(str(context.exception),
                         "Task IDs must be integers.")
        test = self.test_repo.list_tasks()
        result = [
            Task(1, False, 'test', 'test description',
                        self.current_date, None, None),
            Task(4, False, 'test4', 'test4 description',
                        self.current_date, None, None),
            Task(5, False, 'test5', 'test5 description',
                        self.current_date, None, None)
        ]
        self.assertEqual(result, test)

    def test_delete_task_with_correct_then_incorrect_arg_types(self):
        with self.assertRaises(TypeError) as context:
            self.cad.delete_task('five')
        self.assertEqual(str(context.exception),
                         "Task IDs must be integers.")

    def test_delete_task_when_task_id_not_found(self):
        with self.assertRaises(ValueError) as context:
            self.cad.delete_task(5)
        self.assertEqual(str(context.exception),
                         "Task (5) not found.")

    def test_delete_from_task_folder(self):
        self.cad.create_task("test1", "test1 description", "test folder")
        self.cad.create_task("test2", "test2 description", "test folder")
        self.cad.create_task("test3", "test3 description", "other folder")
        test = [
            Task(3, False, 'test3', 'test3 description',
                 self.current_date, 'other folder', None)
            ]
        self.cad.delete_all_from_folder("test folder")
        result = self.test_repo.list_tasks()
        self.assertEqual(result, test)

    def test_delete_from_task_folder_when_folder_does_not_exist(self):
        with self.assertRaises(ValueError) as context:
            self.cad.delete_all_from_folder('five')
        self.assertEqual(str(context.exception),
                         "Task folder not found.")

    def test_delete_from_task_folder_with_multiple_args_given(self):
        self.cad.create_task("test", "test description", "test folder")
        self.cad.create_task("test2", "test2 description", "test folder")
        self.cad.create_task("test3", "test3 description", "test folder2")
        self.cad.create_task("test4", "test4 description", "test folder2")
        self.cad.create_task("test5", "test5 description", "test folder3")
        self.cad.create_task("test6", "test5 description", "test folder4")
        self.cad.create_task("test7", "test5 description", "test folder4")
        test = [
            Task(1, False, 'test', 'test description',
                 self.current_date, 'test folder', None),
            Task(2, False, 'test2', 'test2 description',
                 self.current_date, 'test folder', None),
            Task(5, False, 'test5', 'test5 description',
                 self.current_date, 'test folder3', None),
            ]
        self.cad.delete_all_from_folder('test folder2', 'test folder4')
        result = self.test_repo.list_tasks()
        self.assertEqual(result, test)

    def test_delete_from_task_folder_with_incorrect_arg_types_given(self):
        with self.assertRaises(TypeError) as context:
            self.cad.delete_all_from_folder(5)
        self.assertEqual(str(context.exception),
                         "The Task folder name must be a string.")


if __name__ == "__main__":
    unittest.main()
