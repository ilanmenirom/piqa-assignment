from dataclasses import dataclass


@dataclass
class PiqaProgramConfig:
    extra_instructions: str = ""  # set as empty string to provide no extra instructions
    max_reviews: int = 0  # set as 0 to disable reviews
    verbose: bool = False
    generate_prompt_flag: bool = True
