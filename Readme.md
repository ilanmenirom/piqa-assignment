# PIQA Assignment

## Installation

`pip install langchain_google_genai==0.0.9`

## Run

 
`python main.py GOOGLE_API_KEY=<INSERT_YOUR_API_KEY_HERE!>`
This script tests program accuracy on 50 random questions.

### Configuration
Program configuration defined in `piqa_program_config.py`. Parameters:
* **extra_instructions** (str): Additional text in the LLM prompt
* **max_reviews** (int): Maximum amount of LLM reviews per question (to avoid infinite loop). Set to 0 for no reviews.
* **verbose** (bool): Controls printing prompt, responses and results summary 
* **shuffle_questions** (bool): Controls a random swap between options A and B (see part 2) 

## Assignment Results
Note: Due to limited number of test questions, results are a rough estimation.

### Part 1, Step 2

Accuracy: 74%

### Part 1, Step 3

1. "Think creatively." - 68% Success
2. "Make sure your answer is correct." - 72% Success
3. "You are an expert at physical interaction questions." - 78% Success
4. "I believe in you." - 74% Success
5. "Think what it's like to be in a person's shoes and apply physical commonsense." - 76% Success
6. "Before writing the answer, first describe both options as complete sentences in your own words." - 78% Success

Key takeaways:
* It seems to be somewhat helpful to provide prior information about the dataset challenges (3 and 5).
* Asking the model to rephrase the questions seems to have positive effect on the results (6).
 

### Part 2

Results:
The new success rate is 78% (slightly higher than part 1 step 2).
Review stage analysis: 
* Most of the answers remained unchanged.
* Changes were mostly wrong to right, resulting in a slight improvement

More samples are needed for a more conclusive comparison, though it is resources-intensive.

### Part 2: More?

**1) Swapping The Order of Choices:**

There seems to be a consistent tendency of the LLM to favor answer A.  
To address this, I tried repeating the same question while swapping the order of the choices each time, and then taking the majority of the results.
The experiment involved 4 repetitions per question, 200 prompts in total. The accuracy remained the same, at 74%. 
Perhaps more repetitions might yield some improvement, but it is a time-consuming process.
There is a deprecated code for this method in `piqa_program._answer_question_with_swaps` which can be reviewed if necessary.


**2) Using LLM To Generate Prompt:**

I noticed that the tendency the prefer answer A occurs especially in cases when the choices are long and contain similar words, making it hard to distinguish between them.
To address this, I decided to use another LLM instance to generate a prompt with a clearer distinction between the choices.
In the new architecture I provided the LLM with the question and asked it to generate custom prompt to the specific question, focusing on concise phrasing.
To make sure the answer is parsable, I also included instructions regarding the answer structure. 
The new prompt was given to another LLM instance to answer the question.
The modification resulted in a significant improvement: 86% accuracy. 
It also seemed to finally balance the selection of answers A and B.


## TODOS:
* Test invalid API KEY
* Test no verbose
* Test installation in new environment
