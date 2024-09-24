from typing import Tuple, List

import numpy as np

from consts import QUESTIONS_PATH, ANSWERS_PATH

QUESTIONS_LIST = open(QUESTIONS_PATH, "r").readlines()
ANSWERS_LIST = open(ANSWERS_PATH, "r").readlines()
assert len(QUESTIONS_LIST) == len(ANSWERS_LIST), "Questions and answers should be in the same length"
NUM_SAMPLES = len(ANSWERS_LIST)


class DataLoader:
    @staticmethod
    def get_random_samples(num_samples: int) -> Tuple[List, List]:
        indices = np.random.choice(range(NUM_SAMPLES), size=num_samples, replace=False)
        return [QUESTIONS_LIST[ind] for ind in indices], [int(ANSWERS_LIST[ind]) for ind in indices]
