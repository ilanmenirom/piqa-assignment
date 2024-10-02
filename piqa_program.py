from google.generativeai.types import StopCandidateException
from langchain_google_genai import ChatGoogleGenerativeAI

from consts import SINGLE_ANSWER_PRE_PROMPT_PATH, REVIEW_PRE_PROMPT_PATH, ANSWER_BEFORE_REVIEWS_PRE_PROMPT_PATH, \
    ANSWER_CHOICES, REVIEW_CHOICES, NO_INDEX_KEY, GENERATE_PROMPT_PRE_PROMPT_PATH
from data_loader import load_random_questions_and_answers
from piqa_program_config import PiqaProgramConfig
from utils import convert_response_to_index, get_selected_solution, flip_choices, majority

SINGLE_ANSWER_PRE_PROMPT = open(SINGLE_ANSWER_PRE_PROMPT_PATH, "r").read()
ANSWER_BEFORE_REVIEWS_PRE_PROMPT = open(ANSWER_BEFORE_REVIEWS_PRE_PROMPT_PATH, "r").read()
REVIEW_PRE_PROMPT = open(REVIEW_PRE_PROMPT_PATH, "r").read()
GENERATE_PROMPT_PRE_PROMPT = open(GENERATE_PROMPT_PRE_PROMPT_PATH, "r").read()


class PiqaProgram:
    def __init__(
            self,
            google_api_key: str,
            config: PiqaProgramConfig,
    ):
        self._llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=google_api_key)
        self._config = config

    def get_questions_accuracy(self, num_questions: int) -> float:
        questions, answers = load_random_questions_and_answers(num_questions)
        program_answers = [self._answer_question(question) for question in questions]
        if self._config.verbose:
            print("-------------Summary:---------------")
            [print(f"Question: {question}, expected answer: {answer}, program answer: {model_answer}")
             for question, answer, model_answer in zip(questions, answers, program_answers)]

        n_correct_answers = sum([answer == program_answer for answer, program_answer in zip(answers, program_answers)])
        return n_correct_answers / num_questions

    def _answer_question(self, question: dict) -> int:
        prompt = self._create_initial_prompt(question)
        response = self._invoke_llm(prompt)
        choice_ind = convert_response_to_index(response, ANSWER_CHOICES)
        if choice_ind == NO_INDEX_KEY:
            return choice_ind  # no answer provided, avoid reviewing it

        return self._review_answer(question, response, choice_ind)

    # Deprecated: see Readme.md part 2 for documentation on this part
    def _answer_question_with_swaps(self, question: dict, num_repetitions: int) -> int:
        answers = []
        flipped = False
        for _ in range(num_repetitions):
            choice_ind = self._answer_question(question)
            # inverse index when choices were flipped:
            choice_ind = 1 - choice_ind if flipped and choice_ind != NO_INDEX_KEY else choice_ind
            answers.append(choice_ind)
            question = flip_choices(question)
            flipped = not flipped

        return majority(answers)

    def _invoke_llm(self, prompt: str) -> str:
        try:
            ai_message = self._llm.invoke(prompt)
            response = ai_message.content
        except StopCandidateException as e:
            # Mitigation for LLM content block issue
            response = f"No Answer, due to exception: {e}"

        if self._config.verbose:
            print(f"Prompt: {prompt}")
            print(f"Response: {response}\n\n")

        return response

    def _create_initial_prompt(self, question: dict) -> str:
        if self._config.generate_prompt_flag:
            return self._generate_prompt(question)

        reviews_flag = self._config.max_reviews > 0
        pre_prompt = ANSWER_BEFORE_REVIEWS_PRE_PROMPT if reviews_flag else SINGLE_ANSWER_PRE_PROMPT
        return f"{pre_prompt} {self._config.extra_instructions} {question}"

    def _create_review_prompt(self, question: dict, previous_response: str, choice_ind: int) -> str:
        return (f"{REVIEW_PRE_PROMPT} "
                f"{self._config.extra_instructions} "
                f"Question: {question}. "
                f"Answer: {get_selected_solution(question, choice_ind)}. "
                f"Explanation: {previous_response}")

    def _review_answer(self, question: dict, response: str, choice_ind: int) -> int:
        for _ in range(self._config.max_reviews):
            prompt = self._create_review_prompt(question, response, choice_ind)
            review_response = self._invoke_llm(prompt)
            review_choice_ind = convert_response_to_index(review_response, REVIEW_CHOICES)  # can also be no-answer
            if review_choice_ind == 0:
                return choice_ind  # agreement

            if review_choice_ind == 1:
                choice_ind = 1 - choice_ind
                response = review_response  # keep reasoning of the last choice update

        return choice_ind  # no reviews configured / reviews loop reached maximum iterations

    def _generate_prompt(self, question: dict) -> str:
        generated_prompt = self._invoke_llm(f"{GENERATE_PROMPT_PRE_PROMPT}. Dictionary: {question}")
        # Add answer structure, to make sure its parsable:
        structure_instruction = \
            "Please write your final answer (either A or B) between the <answer> and </answer> tags. "
        return f"{generated_prompt} {structure_instruction} {self._config.extra_instructions}"
