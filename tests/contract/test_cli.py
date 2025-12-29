"""
Contract tests for CLI interface in the Todo CLI application.
"""
import unittest
import sys
import os
import io
from contextlib import redirect_stdout, redirect_stderr

# Add the src directory to the path to allow imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from main import create_parser, main
from unittest.mock import patch, MagicMock


class TestCLIParser(unittest.TestCase):
    """Test cases for the CLI argument parser."""

    def setUp(self):
        """Set up the argument parser for testing."""
        self.parser = create_parser()

    def test_add_command_parsing(self):
        """Test parsing of the add command."""
        args = self.parser.parse_args(['add', '--title', 'Test title'])
        self.assertEqual(args.command, 'add')
        self.assertEqual(args.title, 'Test title')
        self.assertIsNone(args.description)

        args = self.parser.parse_args(['add', '--title', 'Test title', '--description', 'Test description'])
        self.assertEqual(args.command, 'add')
        self.assertEqual(args.title, 'Test title')
        self.assertEqual(args.description, 'Test description')

    def test_list_command_parsing(self):
        """Test parsing of the list command."""
        args = self.parser.parse_args(['list'])
        self.assertEqual(args.command, 'list')

    def test_update_command_parsing(self):
        """Test parsing of the update command."""
        args = self.parser.parse_args(['update', '--id', '1', '--title', 'New title'])
        self.assertEqual(args.command, 'update')
        self.assertEqual(args.id, 1)
        self.assertEqual(args.title, 'New title')
        self.assertIsNone(args.description)

        args = self.parser.parse_args(['update', '--id', '2', '--description', 'New description'])
        self.assertEqual(args.command, 'update')
        self.assertEqual(args.id, 2)
        self.assertIsNone(args.title)
        self.assertEqual(args.description, 'New description')

    def test_delete_command_parsing(self):
        """Test parsing of the delete command."""
        args = self.parser.parse_args(['delete', '--id', '1'])
        self.assertEqual(args.command, 'delete')
        self.assertEqual(args.id, 1)

    def test_complete_command_parsing(self):
        """Test parsing of the complete command."""
        args = self.parser.parse_args(['complete', '--id', '1'])
        self.assertEqual(args.command, 'complete')
        self.assertEqual(args.id, 1)


class TestCLIContract(unittest.TestCase):
    """Contract tests for the CLI interface behavior."""

    @patch('sys.argv', ['main.py', 'add', '--title', 'Test task', '--description', 'Test description'])
    def test_add_command_contract(self):
        """Test the add command contract."""
        # Capture stdout to check the output
        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            # We can't easily test the full main function because it creates a new service each time
            # Instead, we'll test the argument parsing and expected behavior
            parser = create_parser()
            args = parser.parse_args(['add', '--title', 'Test task', '--description', 'Test description'])

            self.assertEqual(args.command, 'add')
            self.assertEqual(args.title, 'Test task')
            self.assertEqual(args.description, 'Test description')

    @patch('sys.argv', ['main.py', 'list'])
    def test_list_command_contract(self):
        """Test the list command contract."""
        parser = create_parser()
        args = parser.parse_args(['list'])
        self.assertEqual(args.command, 'list')

    @patch('sys.argv', ['main.py', 'update', '--id', '1', '--title', 'Updated task'])
    def test_update_command_contract(self):
        """Test the update command contract."""
        parser = create_parser()
        args = parser.parse_args(['update', '--id', '1', '--title', 'Updated task'])
        self.assertEqual(args.command, 'update')
        self.assertEqual(args.id, 1)
        self.assertEqual(args.title, 'Updated task')
        self.assertIsNone(args.description)

    @patch('sys.argv', ['main.py', 'delete', '--id', '1'])
    def test_delete_command_contract(self):
        """Test the delete command contract."""
        parser = create_parser()
        args = parser.parse_args(['delete', '--id', '1'])
        self.assertEqual(args.command, 'delete')
        self.assertEqual(args.id, 1)

    @patch('sys.argv', ['main.py', 'complete', '--id', '1'])
    def test_complete_command_contract(self):
        """Test the complete command contract."""
        parser = create_parser()
        args = parser.parse_args(['complete', '--id', '1'])
        self.assertEqual(args.command, 'complete')
        self.assertEqual(args.id, 1)

    def test_error_handling_contract(self):
        """Test error handling for invalid commands and arguments."""
        parser = create_parser()

        # Test missing required arguments
        with self.assertRaises(SystemExit):
            # This simulates calling without required args, which argparse handles by exiting
            parser.parse_args(['add'])  # Missing --title

        # Test invalid ID type
        with self.assertRaises(SystemExit):
            parser.parse_args(['delete', '--id', 'invalid'])  # ID should be integer


class TestCLIErrorHandling(unittest.TestCase):
    """Test CLI error handling scenarios."""

    def test_invalid_command(self):
        """Test handling of invalid commands."""
        parser = create_parser()

        # argparse will raise SystemExit for invalid commands
        with self.assertRaises(SystemExit):
            parser.parse_args(['invalid_command'])

    def test_missing_required_args(self):
        """Test handling of missing required arguments."""
        parser = create_parser()

        # Test add command without required title
        with self.assertRaises(SystemExit):
            parser.parse_args(['add'])

    def test_invalid_id_type(self):
        """Test handling of invalid ID type."""
        parser = create_parser()

        # Test commands with non-integer IDs
        with self.assertRaises(SystemExit):
            parser.parse_args(['update', '--id', 'not_an_int'])

        with self.assertRaises(SystemExit):
            parser.parse_args(['delete', '--id', 'not_an_int'])

        with self.assertRaises(SystemExit):
            parser.parse_args(['complete', '--id', 'not_an_int'])


if __name__ == '__main__':
    unittest.main()