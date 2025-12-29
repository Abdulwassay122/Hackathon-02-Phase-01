"""
Integration tests for TaskService in the Todo CLI application.
"""
import unittest
import sys
import os

# Add the src directory to the path to allow imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from services.task_service import TaskService


class TestTaskService(unittest.TestCase):
    """Test cases for the TaskService class."""

    def setUp(self):
        """Set up a fresh TaskService for each test."""
        self.service = TaskService()

    def test_add_task_valid(self):
        """Test adding a valid task through the service."""
        task = self.service.add_task("Test title", "Test description")
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test title")
        self.assertEqual(task.description, "Test description")
        self.assertFalse(task.completed)

    def test_add_task_without_description(self):
        """Test adding a task without description through the service."""
        task = self.service.add_task("Test title")
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test title")
        self.assertIsNone(task.description)

    def test_add_task_title_validation(self):
        """Test that adding a task with empty title raises ValueError."""
        with self.assertRaises(ValueError):
            self.service.add_task("")

        with self.assertRaises(ValueError):
            self.service.add_task("   ")

        with self.assertRaises(ValueError):
            self.service.add_task(None)

    def test_get_task_exists(self):
        """Test getting an existing task through the service."""
        task = self.service.add_task("Test title")
        retrieved_task = self.service.get_task(task.id)
        self.assertEqual(retrieved_task.id, task.id)
        self.assertEqual(retrieved_task.title, task.title)

    def test_get_task_not_exists(self):
        """Test getting a non-existent task returns None."""
        result = self.service.get_task(999)
        self.assertIsNone(result)

    def test_get_all_tasks(self):
        """Test getting all tasks through the service."""
        task1 = self.service.add_task("Title 1")
        task2 = self.service.add_task("Title 2")
        task3 = self.service.add_task("Title 3")

        all_tasks = self.service.get_all_tasks()
        self.assertEqual(len(all_tasks), 3)
        # Check that tasks are sorted by ID
        self.assertEqual(all_tasks[0].id, 1)
        self.assertEqual(all_tasks[1].id, 2)
        self.assertEqual(all_tasks[2].id, 3)

    def test_update_task_exists(self):
        """Test updating an existing task through the service."""
        task = self.service.add_task("Original title", "Original description")
        success = self.service.update_task(task.id, "New title", "New description")

        self.assertTrue(success)
        updated_task = self.service.get_task(task.id)
        self.assertEqual(updated_task.title, "New title")
        self.assertEqual(updated_task.description, "New description")

    def test_update_task_partial(self):
        """Test updating only title or description through the service."""
        task = self.service.add_task("Original title", "Original description")

        # Update only title
        success = self.service.update_task(task.id, title="New title")
        self.assertTrue(success)
        updated_task = self.service.get_task(task.id)
        self.assertEqual(updated_task.title, "New title")
        self.assertEqual(updated_task.description, "Original description")

        # Update only description
        success = self.service.update_task(task.id, description="Newer description")
        self.assertTrue(success)
        updated_task = self.service.get_task(task.id)
        self.assertEqual(updated_task.title, "New title")
        self.assertEqual(updated_task.description, "Newer description")

    def test_update_task_title_validation(self):
        """Test that updating with empty title raises ValueError."""
        task = self.service.add_task("Original title")

        with self.assertRaises(ValueError):
            self.service.update_task(task.id, title="")

        with self.assertRaises(ValueError):
            self.service.update_task(task.id, title="   ")

    def test_update_task_not_exists(self):
        """Test updating a non-existent task returns False."""
        success = self.service.update_task(999, "New title")
        self.assertFalse(success)

    def test_delete_task_exists(self):
        """Test deleting an existing task through the service."""
        task = self.service.add_task("Test title")
        success = self.service.delete_task(task.id)

        self.assertTrue(success)
        self.assertIsNone(self.service.get_task(task.id))

    def test_delete_task_not_exists(self):
        """Test deleting a non-existent task returns False."""
        success = self.service.delete_task(999)
        self.assertFalse(success)

    def test_toggle_completion_exists(self):
        """Test toggling completion status of an existing task through the service."""
        task = self.service.add_task("Test title")

        # Initially should be False
        self.assertFalse(task.completed)

        # Toggle should change to True
        success = self.service.toggle_completion(task.id)
        self.assertTrue(success)
        self.assertTrue(task.completed)

        # Toggle again should change back to False
        success = self.service.toggle_completion(task.id)
        self.assertTrue(success)
        self.assertFalse(task.completed)

    def test_toggle_completion_not_exists(self):
        """Test toggling completion status of a non-existent task returns False."""
        success = self.service.toggle_completion(999)
        self.assertFalse(success)


class TestTaskServiceIntegration(unittest.TestCase):
    """Integration tests for the full TaskService workflow."""

    def setUp(self):
        """Set up a fresh TaskService for each test."""
        self.service = TaskService()

    def test_full_workflow_add_update_list_delete(self):
        """Test the complete workflow: add, update, list, delete tasks."""
        # Add multiple tasks
        task1 = self.service.add_task("Task 1", "Description for task 1")
        task2 = self.service.add_task("Task 2", "Description for task 2")
        task3 = self.service.add_task("Task 3")

        # Verify all tasks exist
        all_tasks = self.service.get_all_tasks()
        self.assertEqual(len(all_tasks), 3)

        # Check specific task details
        retrieved_task1 = self.service.get_task(task1.id)
        self.assertEqual(retrieved_task1.title, "Task 1")
        self.assertEqual(retrieved_task1.description, "Description for task 1")
        self.assertFalse(retrieved_task1.completed)

        # Update a task
        update_success = self.service.update_task(task2.id, "Updated Task 2", "Updated description")
        self.assertTrue(update_success)

        # Verify the update worked
        updated_task2 = self.service.get_task(task2.id)
        self.assertEqual(updated_task2.title, "Updated Task 2")
        self.assertEqual(updated_task2.description, "Updated description")

        # Toggle completion status
        toggle_success = self.service.toggle_completion(task1.id)
        self.assertTrue(toggle_success)

        toggled_task = self.service.get_task(task1.id)
        self.assertTrue(toggled_task.completed)

        # Delete a task
        delete_success = self.service.delete_task(task3.id)
        self.assertTrue(delete_success)

        # Verify deletion worked
        all_tasks_after_delete = self.service.get_all_tasks()
        self.assertEqual(len(all_tasks_after_delete), 2)

        # Verify task 3 no longer exists
        self.assertIsNone(self.service.get_task(task3.id))

    def test_id_sequencing(self):
        """Test that IDs are assigned sequentially and properly."""
        task1 = self.service.add_task("Task 1")
        task2 = self.service.add_task("Task 2")
        task3 = self.service.add_task("Task 3")

        # Verify sequential IDs
        self.assertEqual(task1.id, 1)
        self.assertEqual(task2.id, 2)
        self.assertEqual(task3.id, 3)

        # Delete middle task
        self.service.delete_task(task2.id)

        # Add new task - should get next available ID
        task4 = self.service.add_task("Task 4")
        self.assertEqual(task4.id, 4)

        # Verify other tasks still exist with their IDs
        self.assertIsNotNone(self.service.get_task(task1.id))
        self.assertIsNone(self.service.get_task(task2.id))  # Deleted
        self.assertIsNotNone(self.service.get_task(task3.id))
        self.assertIsNotNone(self.service.get_task(task4.id))


if __name__ == '__main__':
    unittest.main()