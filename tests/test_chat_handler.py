import unittest
from unittest.mock import patch, MagicMock, ANY, call
from chat_completions.chat_handler import chat
from helpers.running_env import RunningEnv

class TestChatHandler(unittest.TestCase):
    @patch('builtins.input', create=True)
    @patch('builtins.print')
    @patch('chat_completions.chat_handler.get_openai_client')
    def test_chat_exit_immediately(self, mock_get_openai_client, mock_print, mock_input):
        """
        Test the chat function for immediate exit scenario without sending any message.
        """

        mock_input.side_effect = ['exit']
        # chat(system_prompt="You are a good friend.", model="gpt-4")
        chat(RunningEnv(instructions="You are a good friend.", model="gpt-4"))
        mock_openai_client = MagicMock()
        mock_get_openai_client.assert_called_once_with()
        mock_openai_client.chat.completions.create.assert_not_called()
        expected_calls = [
            call("--------------------------------"),
            call("Enter your message. Press enter twice to send. Type 'exit' to quit."),
            call('\nYou: ', end=''),
            call('Exiting chat. Goodbye!'),
            call('Token count for all the interactions: prompt tokens: 0, completion tokens: 0, total tokens: 0.')
        ]
        mock_print.assert_has_calls(expected_calls, any_order=True)

        # Additionally, you can check the number of print calls if necessary
        self.assertEqual(mock_print.call_count, len(expected_calls))

    @patch('builtins.input', create=True)
    @patch('builtins.print')
    @patch('chat_completions.chat_handler.get_openai_client')
    def test_chat_with_single_message(self, mock_get_openai_client, mock_print, mock_input):
        """
        Test the chat function with a single user message, then exiting.
        """
        # Setup mock for user input to send one message and then 'exit'
        mock_input.side_effect = ['Hello, OpenAI!', '', 'hey', '', 'exit']

        # Mock OpenAI API response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content="Hello, User!"))]
        mock_openai_client = MagicMock()
        mock_openai_client.chat.completions.create().return_value = mock_response

        # Execute chat with mocked dependencies
        chat(RunningEnv(instructions="You are a good friend.", model="gpt-4"))

        mock_get_openai_client.assert_called_once()
        mock_openai_client.chat.completions.create.assert_called_once()


if __name__ == '__main__':
    unittest.main()