import unittest
from unittest.mock import patch, call
from src.prompt_creator import choose_prompt, format_user_input

class TestPromptCreator(unittest.TestCase):
    
    def test_format_user_input(self):
        """Test if format_user_input correctly formats a list of strings into a single string separated by newlines."""
        user_input = ["Hello", "How are you?", "I'm fine, thank you."]
        expected_output = "Hello\nHow are you?\nI'm fine, thank you."
        self.assertEqual(format_user_input(user_input), expected_output)

    @patch('builtins.input', side_effect=['1'])
    @patch('builtins.print')
    def test_choose_prompt_valid_choice(self, mock_print, mock_input):
        """
        Test if choose_prompt returns the correct prompt when a valid choice is made.
        """
        expected_prompt = "You are an assistant."
        self.assertEqual(choose_prompt(), expected_prompt)
        mock_input.assert_called_once_with("Your choice: ")

    @patch('builtins.input', side_effect=['6', '1'])  # Simulate invalid choice followed by a valid choice
    @patch('builtins.print')
    def test_choose_prompt_invalid_then_valid_choice(self, mock_print, mock_input):
        """
        Test if choose_prompt handles invalid choices by notifying the user and then accepting a valid choice.
        """
        expected_prompt = "You are an assistant."
        self.assertEqual(choose_prompt(), expected_prompt)
        expected_calls = [
            call("\n---------------------------\n    Choose a Conversation Starter\n---------------------------"),
            call("1. You are an assistant."),
            call("2. You are a friend giving advice."),
            call("3. You are a tutor explaining a concept."),
            call("4. You are a coach motivating your team."),
            call("5. You are a traveler sharing stories."),
            call("---------------------------"),
            call("Select a number or press enter for a random start."),
            call("Invalid choice, proceeding with a random prompt.")
        ]
        mock_print.assert_has_calls(expected_calls, any_order=True)

    @patch('builtins.input', return_value='')  # Simulate pressing enter without making a selection
    @patch('builtins.print')
    def test_choose_prompt_no_choice(self, mock_print, mock_input):
        """
        Test if choose_prompt correctly defaults to "You are an assistant." when no choice is made.
        """
        expected_prompt = "You are an assistant."
        self.assertEqual(choose_prompt(), expected_prompt)

if __name__ == '__main__':
    unittest.main()