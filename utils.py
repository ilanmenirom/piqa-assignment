import os

from consts import NO_INDEX_KEY, NO_CHOICE_KEY, START_TAG, END_TAG


def get_google_api_key() -> str:
    key = os.environ.get('GOOGLE_API_KEY', None)
    if key is None:
        return input("Insert Google API key:")
    else:
        return key


def convert_response_to_index(answer: str) -> int:
    choice = parse_choice(answer)
    return convert_choice_to_index(choice)


def parse_choice(response: str) -> str:
    start_tag_pos = response.find(START_TAG)
    end_tag_pos = response.find(END_TAG)
    if start_tag_pos == -1 or end_tag_pos == -1:
        return NO_CHOICE_KEY

    return response[start_tag_pos + len(START_TAG):end_tag_pos]


def convert_choice_to_index(choice: str) -> int:
    if choice == "A":
        return 0
    elif choice == "B":
        return 1
    else:
        return NO_INDEX_KEY


def convert_index_to_choice(index: int) -> str:
    if index == 0:
        return "A"
    elif index == 1:
        return "B"
    else:
        return NO_CHOICE_KEY

