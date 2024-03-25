class TokenCounts:
    def __init__(self, total_tokens=0, total_prompt_tokens=0, total_completion_tokens=0):
        self.total_tokens = total_tokens
        self.total_prompt_tokens = total_prompt_tokens
        self.total_completion_tokens = total_completion_tokens

    def print(self):
        print(f'Token count for all the interactions: prompt tokens: {self.total_prompt_tokens}, completion tokens: {self.total_completion_tokens}, total tokens: {self.total_tokens}.')

    def update(self, prompt_tokens, completion_tokens, total_tokens):
        print(f'Token count for this interaction: prompt tokens: {prompt_tokens}, completion tokens: {completion_tokens}, total tokens: {total_tokens}.')
        self.total_prompt_tokens += prompt_tokens
        self.total_completion_tokens += completion_tokens
        self.total_tokens += total_tokens