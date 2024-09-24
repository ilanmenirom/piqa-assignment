from piqa_program import PiqaProgram
from utils import get_google_api_key


def main():
    extra_instructions = ("Before writing the answer, first describe both options as complete sentences in your own "
                          "words. Watch out for physical commonsense - think what it's like to be in a person's shoes "
                          "from a physical perspective.")
    reviewer_extra_instructions = "Change the original answer only when it's an obvious mistake, or when it's absent."
    program = PiqaProgram(
        get_google_api_key(),
        verbose=True,
        initial_extra_instructions=extra_instructions,
        review_extra_instructions=reviewer_extra_instructions,
        max_reviews=5,
    )
    num_questions = 50
    success_rate = program.get_questions_accuracy(num_questions)
    print(f"Success rate for {num_questions} questions: {success_rate * 100:.0f}%")


if __name__ == '__main__':
    main()

