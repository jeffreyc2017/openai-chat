import unittest
from unittest.mock import patch, MagicMock
from src.chat_handler import chat

class TestChatHandler(unittest.TestCase):

    @patch('src.chat_handler.input', create=True)
    @patch('src.chat_handler.print')
    @patch('src.chat_handler.openai_client')
    def test_chat_exit_immediately(self, mock_openai_client, mock_print, mock_input):
        """
        Test the chat function for immediate exit scenario.
        """
        # Mock user input to simulate 'exit' input immediately
        mock_input.side_effect = ['exit']

        # Mock OpenAI client's chat.completions.create() method
        mock_openai_client.chat.completions.create = MagicMock()

        # Call the chat function with mock parameters
        chat(mock_openai_client, "You are an assistant.", "gpt-3.5-turbo")

        # Assertions
        mock_input.assert_called()
        mock_openai_client.chat.completions.create.assert_not_called()
        mock_print.assert_any_call("\nExiting chat. Goodbye! Total tokens used: 0")

    @patch('src.chat_handler.num_tokens_from_messages', return_value=10)
    @patch('src.chat_handler.input', create=True)
    @patch('src.chat_handler.print')
    @patch('src.chat_handler.openai_client')
    def test_chat_with_user_message(self, mock_openai_client, mock_print, mock_input, mock_token_counter):
        """
        Test the chat function with a user sending a message and then exiting.
        """
        # Mock user input to simulate sending one message and then exiting
        mock_input.side_effect = ['Hello, AI!', 'exit']

        # Mock OpenAI client's chat.completions.create() method to simulate a response
        mock_openai_client.chat.completions.create = MagicMock(return_value=MagicMock(choices=[MagicMock(message=MagicMock(content="Hello, Human!"))]))

        # Call the chat function with mock parameters
        chat(mock_openai_client, "You are an assistant.", "gpt-3.5-turbo")

        # Assertions
        mock_openai_client.chat.completions.create.assert_called_once()
        mock_print.assert_any_call("\rAI: ", end="")
        mock_print.assert_any_call("Hello, Human!")
        mock_token_counter.assert_called()
        mock_print.assert_any_call("\nExiting chat. Goodbye! Total tokens used: 10")

if __name__ == '__main__':
    unittest.main()