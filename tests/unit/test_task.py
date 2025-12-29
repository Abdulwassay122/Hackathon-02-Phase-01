"""
Unit tests for Task model and TaskCollection in the Todo CLI application.
"""
import unittest
from src.models.task import Task, TaskCollection


class TestTask(unittest.TestCase):
    """Test cases for the Task class."""

    def test_task_creation_valid(self):
        """Test creating a task with valid parameters."""
        task = Task(1, "Test title", "Test description")
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test title")
        self.assertEqual(task.description, "Test description")
        self.assertFalse(task.completed)

    def test_task_creation_without_description(self):
        """Test creating a task without description."""
        task = Task(1, "Test title")
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test title")
        self.assertIsNone(task.description)
        self.assertFalse(task.completed)

    def test_task_title_validation(self):
        """Test that creating a task with empty title raises ValueError."""
        with self.assertRaises(ValueError):
            Task(1, "")

        with self.assertRaises(ValueError):
            Task(1, "   ")

        with self.assertRaises(ValueError):
            Task(1, None)


class TestTaskCollection(unittest.TestCase):
    """Test cases for the TaskCollection class."""

    def setUp(self):
        """Set up a fresh TaskCollection for each test."""
        self.collection = TaskCollection()

    def test_add_task_valid(self):
        """Test adding a valid task."""
        task = self.collection.add_task("Test title", "Test description")
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test title")
        self.assertEqual(task.description, "Test description")
        self.assertFalse(task.completed)
        self.assertIn(1, self.collection.tasks)

    def test_add_task_without_description(self):
        """Test adding a task without description."""
        task = self.collection.add_task("Test title")
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test title")
        self.assertIsNone(task.description)

    def test_add_task_title_validation(self):
        """Test that adding a task with empty title raises ValueError."""
        with self.assertRaises(ValueError):
            self.collection.add_task("")

        with self.assertRaises(ValueError):
            self.collection.add_task("   ")

        with self.assertRaises(ValueError):
            self.collection.add_task(None)

    def test_get_task_exists(self):
        """Test getting an existing task."""
        task = self.collection.add_task("Test title")
        retrieved_task = self.collection.get_task(task.id)
        self.assertEqual(retrieved_task.id, task.id)
        self.assertEqual(retrieved_task.title, task.title)

    def test_get_task_not_exists(self):
        """Test getting a non-existent task returns None."""
        result = self.collection.get_task(999)
        self.assertIsNone(result)

    def test_update_task_exists(self):
        """Test updating an existing task."""
        task = self.collection.add_task("Original title", "Original description")
        success = self.collection.update_task(task.id, "New title", "New description")

        self.assertTrue(success)
        updated_task = self.collection.get_task(task.id)
        self.assertEqual(updated_task.title, "New title")
        self.assertEqual(updated_task.description, "New description")

    def test_update_task_partial(self):
        """Test updating only title or description."""
        task = self.collection.add_task("Original title", "Original description")

        # Update only title
        success = self.collection.update_task(task.id, title="New title")
        self.assertTrue(success)
        updated_task = self.collection.get_task(task.id)
        self.assertEqual(updated_task.title, "New title")
        self.assertEqual(updated_task.description, "Original description")

        # Update only description
        success = self.collection.update_task(task.id, description="Newer description")
        self.assertTrue(success)
        updated_task = self.collection.get_task(task.id)
        self.assertEqual(updated_task.title, "New title")
        self.assertEqual(updated_task.description, "Newer description")

    def test_update_task_title_validation(self):
        """Test that updating with empty title raises ValueError."""
        task = self.collection.add_task("Original title")

        with self.assertRaises(ValueError):
            self.collection.update_task(task.id, title="")

        with self.assertRaises(ValueError):
            self.collection.update_task(task.id, title="   ")

    def test_update_task_not_exists(self):
        """Test updating a non-existent task returns False."""
        success = self.collection.update_task(999, "New title")
        self.assertFalse(success)

    def test_delete_task_exists(self):
        """Test deleting an existing task."""
        task = self.collection.add_task("Test title")
        success = self.collection.delete_task(task.id)

        self.assertTrue(success)
        self.assertNotIn(task.id, self.collection.tasks)
        self.assertIsNone(self.collection.get_task(task.id))

    def test_delete_task_not_exists(self):
        """Test deleting a non-existent task returns False."""
        success = self.collection.delete_task(999)
        self.assertFalse(success)

    def test_get_all_tasks(self):
        """Test getting all tasks."""
        task1 = self.collection.add_task("Title 1")
        task2 = self.collection.add_task("Title 2")
        task3 = self.collection.add_task("Title 3")

        all_tasks = self.collection.get_all_tasks()
        self.assertEqual(len(all_tasks), 3)
        # Check that tasks are sorted by ID
        self.assertEqual(all_tasks[0].id, 1)
        self.assertEqual(all_tasks[1].id, 2)
        self.assertEqual(all_tasks[2].id, 3)

    def test_toggle_completion_exists(self):
        """Test toggling completion status of an existing task."""
        task = self.collection.add_task("Test title")

        # Initially should be False
        self.assertFalse(task.completed)

        # Toggle should change to True
        success = self.collection.toggle_completion(task.id)
        self.assertTrue(success)
        self.assertTrue(task.completed)

        # Toggle again should change back to False
        success = self.collection.toggle_completion(task.id)
        self.assertTrue(success)
        self.assertFalse(task.completed)

    def test_toggle_completion_not_exists(self):
        """Test toggling completion status of a non-existent task returns False."""
        success = self.collection.toggle_completion(999)
        self.assertFalse(success)


if __name__ == '__main__':
    unittest.main()