import unittest
from unittest.mock import patch, call
from helpers.prompt_creator import choose_prompt
from chat_completions.chat_handler import format_user_input

class TestPromptCreator(unittest.TestCase):

    def test_format_user_input(self):
        """Test if format_user_input correctly formats a list of strings into a single string separated by newlines."""
        user_input = ["Hello", "How are you?", "I'm fine, thank you."]
        expected_output = "Hello\nHow are you?\nI'm fine, thank you."
        self.assertEqual(format_user_input(user_input), expected_output)

    @patch('builtins.input', side_effect=['2', '1'])  # Choose the first category and the first prompt
    @patch('builtins.print')
    def test_choose_prompt_valid_category_and_prompt(self, mock_print, mock_input):
        """
        Test choosing a valid category and prompt.
        """
        expected_prompt = (
            "Old Friend Chat",
            "Act as an old friend reminiscing about past experiences together.",
            "Maintain a friendly and nostalgic tone throughout the conversation."
        )
        prompt = choose_prompt()
        self.assertEqual(prompt, expected_prompt)

    @patch('builtins.input', side_effect=['1', 'My custom prompt', 'My custom run instructions'])  # Invalid choice, then choose Custom, and enter a custom prompt
    @patch('builtins.print')
    def test_choose_prompt_custom_prompt(self, mock_print, mock_input):
        """
        Test the flow for choosing the 'Custom' category and entering a custom prompt.
        """
        prompt = choose_prompt()
        self.assertEqual(prompt, ('Custom Assistant', 'My custom prompt', 'My custom run instructions'))

    @patch('builtins.input', side_effect=['999', '1', '1'])  # Initially invalid choice, then valid category and prompt
    @patch('builtins.print')
    def test_choose_prompt_invalid_then_valid_choice(self, mock_print, mock_input):
        """
        Test handling of an initial invalid choice followed by a valid category and prompt selection.
        """
        expected_prompt = (None, None, None)
        prompt = choose_prompt()
        self.assertEqual(prompt, expected_prompt)

if __name__ == '__main__':
    unittest.main()