import argparse
from collections import Counter
from typing import Tuple, List

from consts import NO_INDEX_KEY, NO_CHOICE_KEY, START_TAG, END_TAG


def get_google_api_key() -> str:
    parser = argparse.ArgumentParser()
    parser.add_argument("--key", help="Specify Google API key", default=None)
    key = parser.parse_args().key
    return key if key else input("Insert Google API key:")


def calculate_accuracy(list1: List, list2: List) -> float:
    assert len(list1) == len(list2), "When calculation accuracy, lists must have the same length"
    num_accurate = sum([x1 == x2 for x1, x2 in zip(list1, list2)])
    return num_accurate / len(list1)


def convert_response_to_index(answer: str, options: Tuple[str, str]) -> int:
    choice = parse_choice(answer)
    return convert_choice_to_index(choice, options)


def parse_choice(response: str) -> str:
    start_tag_pos = response.find(START_TAG)
    end_tag_pos = response.find(END_TAG)
    if start_tag_pos == -1 or end_tag_pos == -1:
        return NO_CHOICE_KEY

    return response[start_tag_pos + len(START_TAG):end_tag_pos]


def convert_choice_to_index(choice: str, options: Tuple[str, str]) -> int:
    if choice in options:
        return options.index(choice)
    else:
        return NO_INDEX_KEY


def get_selected_solution(question: dict, choice_ind: int) -> str:
    solution_key = f'sol{choice_ind + 1}'
    return NO_CHOICE_KEY if choice_ind == NO_INDEX_KEY else question[solution_key]


def flip_choices(question: dict) -> dict:
    question['sol1'], question['sol2'] = question['sol2'], question['sol1']
    return question


def majority(list_in: List[int]) -> int:
    return Counter(list_in).most_common(1)[0][0]
