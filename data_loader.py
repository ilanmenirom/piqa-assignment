import json
import random
from typing import Tuple

from consts import QUESTIONS_PATH, ANSWERS_PATH


class DataLoader:
    def __init__(self):

        with open(QUESTIONS_PATH, "r") as f:
            questions = [json.loads(line) for line in f.readlines()]

        with open(ANSWERS_PATH, "r") as f:
            answers = [int(line) for line in f.readlines()]

        assert len(questions) == len(answers), f"Questions and answers should be in the same length"
        self._qa_pairs = list(zip(questions, answers))

    # Return two lists, one for questions and one for answers:
    def load_random_questions_and_answers(self, num_samples: int) -> Tuple:
        return zip(*random.sample(self._qa_pairs, num_samples))
