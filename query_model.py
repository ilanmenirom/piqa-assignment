from typing import Optional

import numpy as np
from langchain_google_genai import ChatGoogleGenerativeAI

from consts import INVALID_DIGIT, PRE_PROMPT_PATH, START_TAG, END_TAG, NO_CHOICE_STR
from data_loader import DataLoader

PRE_PROMPT = open(PRE_PROMPT_PATH, "r").read()


class QueryModel:
    def __init__(self, google_api_key: str, verbose: bool = False):
        self._llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=google_api_key)
        self._verbose = verbose

    def get_questions_accuracy(self, num_questions: int) -> float:
        questions_list, answers_list = DataLoader.get_random_samples(num_questions)
        model_answers_list = [self._get_answer_ind(question) for question in questions_list]
        return float(np.mean(np.array(answers_list) == np.array(model_answers_list)))

    def _get_answer_ind(self, question: str) -> int:
        query = QueryModel._build_query_from_question(question)
        answer = self._invoke_llm(query)
        return self._convert_answer_to_index(answer)

    def _invoke_llm(self, query: str) -> str:
        try:
            ai_message = self._llm.invoke(query)
            response = ai_message.content
        except Exception as e:
            response = f"No response, due to exception during LLM invoke: {e}"

        if self._verbose:
            print(f"Query: {query}")
            print(f"Response: {response}")

        return response

    @staticmethod
    def _convert_answer_to_index(answer: str) -> Optional[int]:
        choice = QueryModel._parse_choice(answer)
        return QueryModel._convert_choice_to_index(choice)

    @staticmethod
    def _build_query_from_question(question: str) -> str:
        return f"{PRE_PROMPT}. {question}"

    @staticmethod
    def _parse_choice(answer: str) -> str:
        start_tag_pos = answer.find(START_TAG)
        end_tag_pos = answer.find(END_TAG)
        if start_tag_pos == -1 or end_tag_pos == -1:
            return NO_CHOICE_STR

        return answer[start_tag_pos+len(START_TAG):end_tag_pos]

    @staticmethod
    def _convert_choice_to_index(choice: str) -> int:
        if choice == "A":
            return 0
        elif choice == "B":
            return 1
        else:
            return INVALID_DIGIT
