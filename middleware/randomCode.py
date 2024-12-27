import os
import random

class randomCode:
    def __init__(self):
        self.random_code_len = int(os.getenv("RANDOM_CODE_LENGTH"))
        self.random_code_str = os.getenv("RANDOM_CODE_STR")

    def generate(self):
        return ''.join(self.random_code_str[i] for i in [random.randint(0, len(self.random_code_str) - 1) for _ in range(self.random_code_len)])