import unittest
from unittest.mock import patch, call
from src.model_selector import list_models, choose_model

class TestModelSelector(unittest.TestCase):
    
    def test_list_models(self):
        """Test if list_models returns the expected list of model names."""
        expected_models = [
            "gpt-3.5-turbo",
            "gpt-3.5-turbo-instruct",
            "gpt-4",
            "gpt-4-32k",
            "gpt-4-turbo-preview",
        ]
        self.assertEqual(list_models(), expected_models)

    @patch('builtins.input', side_effect=['1'])
    @patch('builtins.print')
    def test_choose_model_first_option(self, mock_print, mock_input):
        """
        Test if choose_model correctly returns the first model when the user inputs '1'.
        """
        self.assertEqual(choose_model(), "gpt-3.5-turbo")
        mock_input.assert_called_once_with("Select a number to choose a model:")
        
        # Ensure the introduction print statement is called
        mock_print.assert_called()

    @patch('builtins.input', side_effect=['6', '1'])  # User first inputs an invalid choice, then corrects it.
    @patch('builtins.print')
    def test_choose_model_invalid_then_valid_choice(self, mock_print, mock_input):
        """
        Test if choose_model handles an invalid choice followed by a valid choice correctly.
        """
        self.assertEqual(choose_model(), "gpt-3.5-turbo")
        expected_print_calls = [
            call("Invalid choice. Please enter a number from the list.")
        ]
        mock_print.assert_has_calls(expected_print_calls)

if __name__ == '__main__':
    unittest.main()