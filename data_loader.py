import json
import random
from typing import Tuple

from consts import QUESTIONS_PATH, ANSWERS_PATH

# Load the static dataset:
questions = [json.loads(line) for line in open(QUESTIONS_PATH, "r").readlines()]
answers = [int(line) for line in open(ANSWERS_PATH, "r").readlines()]
assert len(questions) == len(answers), "Questions and answers should be in the same length"
qa_pairs = list(zip(questions, answers))


# Return two lists, one for questions and one for answers
def load_random_questions_and_answers(num_samples: int) -> Tuple:
    return zip(*random.sample(qa_pairs, num_samples))
