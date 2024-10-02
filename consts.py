NO_INDEX_KEY = -1
NO_CHOICE_KEY = "NONE"
START_TAG = "<answer>"
END_TAG = "</answer>"
ANSWER_CHOICES = ("A", "B")
REVIEW_CHOICES = ("Correct", "Incorrect")
STRUCTURE_INSTRUCTION = "Please write your final answer (either A or B) between the <answer> and </answer> tags. "

# Pre-Prompts Paths:
QUESTIONS_PATH = "piqa_datasets/questions.txt"
ANSWERS_PATH = "piqa_datasets/answers.txt"
PRE_PROMPTS_PATH = 'pre_prompts'
SINGLE_ANSWER_FILE = "single_answer.txt"
ANSWER_BEFORE_REVIEWS_FILE = "answer_before_reviews.txt"
REVIEW_FILE = "review.txt"
GENERATE_PROMPT_FILE = "generate_prompt.txt"
