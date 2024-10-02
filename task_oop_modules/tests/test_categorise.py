import sqlite3
import unittest
from datetime import date
from src.categorise.categorise import Categorise
from src.task_repo.task_repo import TaskRepository
from src.create_and_delete.create_and_delete import CreateAndDelete
from src.task_repo.task_repo import Task


class TestCategorise(unittest.TestCase):

    def setUp(self):
        self.test_conn = sqlite3.connect(":memory:")
        self.test_repo = TaskRepository(self.test_conn)
        self.test_repo.initialise_database()
        self.current_date = date.today().isoformat()
        self.cat = Categorise(self.test_repo)
        self.cad = CreateAndDelete(self.test_repo)
        # Link the repository to the Cat and CaD instances
        self.cad.task_repository = self.test_repo
        self.cat.task_repository = self.test_repo

    def tearDown(self):
        self.test_conn.close()

    def test_update_folder(self):
        self.cad.create_task("test1", "test1 description", "test1 folder")
        self.cat.update_folder(1, 'changed folder')
        test = [
            Task(1, False, 'test1', 'test1 description',
                 self.current_date, 'changed folder', None)
            ]
        result = self.test_repo.list_tasks()
        self.assertEqual(result, test)

    def test_update_folder_with_no_args_given(self):
        with self.assertRaises(ValueError) as context:
            self.cat.update_folder()
        self.assertEqual(str(context.exception),
                         "Please enter a valid Task ID.")

    def test_update_folder_with_incorrect_task_id_given(self):
        with self.assertRaises(ValueError) as context:
            self.cat.update_folder(5)
        self.assertEqual(str(context.exception),
                         "No Task found with Task ID (5).")

    def test_update_folder_with_both_args_incorrect_task_id_given(self):
        with self.assertRaises(ValueError) as context:
            self.cat.update_folder(6, 'new folder')
        self.assertEqual(str(context.exception),
                         "No Task found with Task ID (6).")

    def test_update_folder_with_incorrect_arg_types_given(self):
        with self.assertRaises(TypeError) as context:
            self.cat.update_folder('Four')
        self.assertEqual(str(context.exception),
                         "Please enter valid arguments. "
                            "Task ID (Mandatory): int; "
                            "Task folder (Optional): str")

    def test_update_folder_with_both_args_incorrect_types_given(self):
        with self.assertRaises(TypeError) as context:
            self.cat.update_folder('Four', 6)
        self.assertEqual(str(context.exception),
                         "Please enter valid arguments. "
                            "Task ID (Mandatory): int; "
                            "Task folder (Optional): str")

    def test_update_folder_to_clear_task_folder(self):
        self.cad.create_task("test1", "test1 description", "test1 folder")
        self.cat.update_folder(1)
        test = [
            Task(1, False, 'test1', 'test1 description',
                 self.current_date, None, None)
            ]
        result = self.test_repo.list_tasks()
        self.assertEqual(result, test)

# ----------------------------------------
    def test_priority_tag(self):
        self.cad.create_task("test1", "test1 description")
        self.cat.update_priority(1, 'high')
        test = [
            Task(1, False, 'test1', 'test1 description',
                 self.current_date, None, 'high')
            ]
        result = self.test_repo.list_tasks()
        self.assertEqual(result, test)

    def test_update_priority_with_no_args_given(self):
        with self.assertRaises(ValueError) as context:
            self.cat.update_priority()
        self.assertEqual(str(context.exception),
                         "Please enter a valid Task ID.")

    def test_update_priority_with_incorrect_task_id_given(self):
        with self.assertRaises(ValueError) as context:
            self.cat.update_priority(2)
        self.assertEqual(str(context.exception),
                         "No Task found with Task ID (2).")

    def test_update_priority_with_both_args_incorrect_task_id_given(self):
        with self.assertRaises(ValueError) as context:
            self.cat.update_priority(8, 'low')
        self.assertEqual(str(context.exception),
                         "No Task found with Task ID (8).")

    def test_update_priority_with_incorrect_arg_types_given(self):
        with self.assertRaises(TypeError) as context:
            self.cat.update_priority('Four')
        self.assertEqual(str(context.exception),
                         "Please enter valid arguments. "
                            "Task ID (Mandatory): int; "
                            "Priority tag (Optional): str")

    def test_update_priority_with_both_args_incorrect_types_given(self):
        with self.assertRaises(TypeError) as context:
            self.cat.update_priority('Four', 6)
        self.assertEqual(str(context.exception),
                         "Please enter valid arguments. "
                            "Task ID (Mandatory): int; "
                            "Priority tag (Optional): str")

    def test_update_priority_to_clear_task_folder(self):
        self.cad.create_task("test1", "test1 description", "new folder", "high")
        self.cat.update_priority(1)
        test = [
            Task(1, False, 'test1', 'test1 description',
                 self.current_date, "new folder", None)
            ]
        result = self.test_repo.list_tasks()
        self.assertEqual(result, test)


if __name__ == "__main__":
    unittest.main()
