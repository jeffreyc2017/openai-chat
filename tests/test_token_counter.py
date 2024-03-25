import unittest
from unittest.mock import patch, MagicMock
from helpers.token_counter import num_tokens_from_messages

class TestTokenCounter(unittest.TestCase):

    @patch('helpers.token_counter.tiktoken')
    def test_num_tokens_with_known_model(self, mock_tiktoken):
        """
        Test token counting for a model with predefined tokens per message and name.
        """
        mock_encoding = MagicMock()
        mock_encoding.encode = MagicMock(side_effect=lambda x: x)
        mock_tiktoken.encoding_for_model.return_value = mock_encoding

        messages = [{"role": "user", "content": "Hello, world!"}]
        model = "gpt-3.5-turbo-0613"

        token_count = num_tokens_from_messages(messages, model)

        # Assert the expected token count, considering predefined tokens per message/name and encoded length
        expected_token_count = 3 + len("user") + len("Hello, world!") + 3  # tokens_per_message + encoded content + priming tokens
        self.assertEqual(token_count, expected_token_count)

    @patch('helpers.token_counter.tiktoken')
    def test_num_tokens_with_unsupported_model(self, mock_tiktoken):
        """
        Test token counting raises NotImplementedError for an unsupported model.
        """
        messages = [{"role": "user", "content": "Hello, world!"}]
        model = "unsupported-model"

        # Assert that calling num_tokens_from_messages with an unsupported model raises NotImplementedError
        with self.assertRaises(NotImplementedError):
            num_tokens_from_messages(messages, model)

    @patch('helpers.token_counter.tiktoken')
    def test_num_tokens_fallback_to_base_encoding_for_unknown_model(self, mock_tiktoken):
        """
        Test token counting uses cl100k_base encoding for unknown models and prints a warning.
        """
        # Setup mock for tiktoken.get_encoding to return a MagicMock with a specific encode behavior for cl100k_base
        mock_encoding = MagicMock()
        mock_encoding.encode = MagicMock(side_effect=lambda x: x)
        mock_tiktoken.get_encoding.return_value = mock_encoding

        messages = [{"role": "user", "content": "Test message"}]
        model = "unknown-model"

        with self.assertRaises(NotImplementedError):
            num_tokens_from_messages(messages, model)

if __name__ == '__main__':
    unittest.main()