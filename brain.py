import google.generativeai as genai
import enum
from quizz_questions import quiz_questions
import time


class AnswerIndex(enum.Enum):
    ZERO = "0"
    ONE = "1"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"


def answer_quiz_question(question: str, answer_choices: list[str]) -> int:
    # Initialize the model
    model = genai.GenerativeModel("gemini-1.5-pro-latest")

    # Format the prompt to clearly include the question and answer choices
    prompt = f"Question: {question}\nChoices:\n"
    for i, choice in enumerate(answer_choices, start=0):
        prompt += f"{i}. {choice}\n"
    prompt += "Choose the best answer (provide the number):"

    # Generate the answer
    answer = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            response_mime_type="text/x.enum",
            response_schema=AnswerIndex,
            max_output_tokens=2,
            temperature=1.0,
        ),
    )

    return int(answer.text)


if __name__ == "__main__":
    for quiz_question in quiz_questions:
        question = quiz_question.question
        answer_choices = quiz_question.answer_choices
        correct_answer_index = quiz_question.correct_answer_index
        print(question)
        print(answer_choices)
        print()
        answer = answer_quiz_question(question, answer_choices)
        is_correct_answer = correct_answer_index == answer
        answer_status = "✅" if is_correct_answer else "❌"
        print(f"{answer_status} {answer_choices[answer]}")
        time.sleep(25)
