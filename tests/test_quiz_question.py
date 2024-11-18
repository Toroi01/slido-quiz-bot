import pytest
from slido_quiz_bot.quizz_question import QuizQuestion


@pytest.fixture
def quiz_questions():
  """
  Fixture to create a list of QuizQuestion instances for testing.
  """
  return [
    QuizQuestion(
      question="What is the capital of France?",
      answer_choices=["Berlin", "Madrid", "Paris", "Rome"],
      correct_answer_index=2,  # Paris is the correct answer
    ),
    QuizQuestion(
      question="Which planet is known as the Red Planet?",
      answer_choices=["Earth", "Mars", "Jupiter", "Saturn"],
      correct_answer_index=1,  # Mars is the correct answer
    ),
    QuizQuestion(
      question="What is the largest ocean on Earth?",
      answer_choices=["Atlantic Ocean", "Indian Ocean", "Arctic Ocean", "Pacific Ocean"],
      correct_answer_index=3,  # Pacific Ocean is the correct answer
    ),
    QuizQuestion(
      question="Who wrote 'Romeo and Juliet'?",
      answer_choices=["Charles Dickens", "Jane Austen", "Mark Twain", "William Shakespeare"],
      correct_answer_index=3,  # William Shakespeare is the correct answer
    ),
    QuizQuestion(
      question="Which element has the chemical symbol 'O'?",
      answer_choices=["Osmium", "Oxygen", "Gold", "Iron"],
      correct_answer_index=1,  # Oxygen is the correct answer
    ),
    QuizQuestion(
      question="What is the hardest natural mineral?",
      answer_choices=["Diamond", "Ruby", "Sapphire", "Emerald"],
      correct_answer_index=0,  # Diamond is the correct answer
    ),
    QuizQuestion(
      question="In which year did the Titanic sink?",
      answer_choices=["1910", "1912", "1914", "1916"],
      correct_answer_index=1,  # 1912 is the correct answer
    ),
    QuizQuestion(
      question="Which gas do plants absorb from the atmosphere?",
      answer_choices=["Oxygen", "Carbon Dioxide", "Nitrogen", "Hydrogen", "Gold"],
      correct_answer_index=1,  # Carbon Dioxide is the correct answer
    ),
    QuizQuestion(
      question="What is the main ingredient in guacamole?",
      answer_choices=["Avocado", "Lemon"],
      correct_answer_index=0,  # Avocado is the correct answer
    ),
    QuizQuestion(
      question="Who painted the Mona Lisa?",
      answer_choices=["Vincent Van Gogh", "Pablo Picasso", "Leonardo da Vinci"],
      correct_answer_index=2,  # Leonardo da Vinci is the correct answer
    ),
  ]


def test_quiz_question_creation(quiz_questions):
  """
  Test the creation of QuizQuestion instances and validate correct_answer_index.
  """
  # Ensure that each QuizQuestion is correctly created
  for idx, quiz in enumerate(quiz_questions):
    assert isinstance(quiz, QuizQuestion), f"QuizQuestion {idx} is not an instance of QuizQuestion"
    assert isinstance(quiz.question, str), f"QuizQuestion {idx} 'question' should be a string"
    assert isinstance(quiz.answer_choices, list), f"QuizQuestion {idx} 'answer_choices' should be a list"
    assert isinstance(quiz.correct_answer_index, int), f"QuizQuestion {idx} 'correct_answer_index' should be an integer"
    assert 0 <= quiz.correct_answer_index < len(quiz.answer_choices), f"QuizQuestion {idx} 'correct_answer_index' is out of bounds"


def test_answer_choices_length(quiz_questions):
  """
  Test that the length of answer_choices is consistent with the number of options for each quiz question.
  """
  for quiz in quiz_questions:
    assert len(quiz.answer_choices) > 0, f"Quiz question '{quiz.question}' has no answer choices."
    assert isinstance(quiz.answer_choices, list), f"Answer choices for '{quiz.question}' is not a list."


def test_correct_answer_index(quiz_questions):
  """
  Test that the correct_answer_index corresponds to a valid answer choice for each question.
  """
  for quiz in quiz_questions:
    correct_answer = quiz.answer_choices[quiz.correct_answer_index]
    assert correct_answer, f"Quiz question '{quiz.question}' has an invalid correct answer choice."
