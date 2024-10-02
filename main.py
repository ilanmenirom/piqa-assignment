from piqa_program import PiqaProgram
from piqa_program_config import PiqaProgramConfig
from utils import get_google_api_key


def main():
    program = PiqaProgram(get_google_api_key(), PiqaProgramConfig())
    num_questions = 50
    success_rate = program.get_questions_accuracy(num_questions)
    print(f"Success rate for {num_questions} questions: {success_rate * 100:.0f}%")


if __name__ == '__main__':
    main()
