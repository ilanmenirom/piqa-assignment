from typing import Tuple

import numpy as np
from langchain_google_genai import ChatGoogleGenerativeAI

from consts import INITIAL_ANSWER_PRE_PROMPT_PATH, REVIEW_ANSWER_PRE_PROMPT_PATH, START_TAG, END_TAG, NO_CHOICE_KEY, \
    NO_INDEX_KEY
from data_loader import DataLoader
from utils import convert_response_to_index

INITIAL_ANSWER_PRE_PROMPT = open(INITIAL_ANSWER_PRE_PROMPT_PATH, "r").read()
REVIEW_ANSWER_PRE_PROMPT = open(REVIEW_ANSWER_PRE_PROMPT_PATH, "r").read()


class PiqaProgram:
    def __init__(
            self,
            google_api_key: str,
            initial_extra_instructions: str = "",
            review_extra_instructions: str = "",
            verbose: bool = False,
            max_reviews: int = 0
    ):
        self._llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=google_api_key)
        self._initial_extra_instructions = initial_extra_instructions
        self._review_extra_instructions = review_extra_instructions
        self._verbose = verbose
        self._max_reviews = max_reviews

    def get_questions_accuracy(self, num_questions: int) -> float:
        questions_list, answers_list = DataLoader.get_random_samples(num_questions)
        model_answers_list = [self._answer_question(question) for question in questions_list]
        if self._verbose:
            print("-------------Summary:---------------")
            [print(f"Questions: {question}, answer: {answer}, model answer: {model_answer}")
             for question, answer, model_answer in zip(questions_list, answers_list, model_answers_list)]

        return float(np.mean(np.array(answers_list) == np.array(model_answers_list)))

    def _answer_question(self, question: str) -> int:
        prompt = self._create_initial_prompt(question)
        response = self._invoke_llm(prompt)
        choice_ind = convert_response_to_index(response)
        for _ in range(self._max_reviews):
            prompt = self._create_review_prompt(question, response)
            response = self._invoke_llm(prompt)
            previous_choice_ind, choice_ind = choice_ind, convert_response_to_index(response)
            if choice_ind == previous_choice_ind or choice_ind == NO_INDEX_KEY:
                # Note that if new choice is unavailable, we prefer the previous choice
                return previous_choice_ind

        return choice_ind

    def _invoke_llm(self, prompt: str) -> str:
        try:
            ai_message = self._llm.invoke(prompt)
            response = ai_message.content
        except Exception as e:
            response = f"No response, due to exception during LLM invoke: {e}"

        if self._verbose:
            print(f"Prompt: {prompt}")
            print(f"Response: {response}\n\n")

        return response

    def _create_initial_prompt(self, question: str) -> str:
        return f"{INITIAL_ANSWER_PRE_PROMPT}. {self._initial_extra_instructions} {question}"

    def _create_review_prompt(self, question: str, previous_response: str) -> str:
        return f"{REVIEW_ANSWER_PRE_PROMPT}. {self._review_extra_instructions} {question}. Answer: {previous_response}"
