import numpy as np

from query_model import QueryModel
from utils import get_google_api_key


def main_part1():
    np.random.seed(42)
    model = QueryModel(get_google_api_key(), verbose=True)
    num_questions = 50
    success_rate = model.get_questions_accuracy(num_questions)
    print(f"Success rate for {num_questions}: {success_rate * 100:.0f}%")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main_part1()

