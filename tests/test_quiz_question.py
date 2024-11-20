from slido_quiz_bot.quizz_question import QuizQuestion


def test_quiz_question_creation(dummy_quiz_questions):
  """
  Test the creation of QuizQuestion instances and validate correct_answer_index.
  """
  # Ensure that each QuizQuestion is correctly created
  for idx, quiz in enumerate(dummy_quiz_questions):
    assert isinstance(quiz, QuizQuestion), f"QuizQuestion {idx} is not an instance of QuizQuestion"
    assert isinstance(quiz.question, str), f"QuizQuestion {idx} 'question' should be a string"
    assert isinstance(quiz.answer_choices, list), f"QuizQuestion {idx} 'answer_choices' should be a list"
    assert isinstance(quiz.correct_answer_index, int), f"QuizQuestion {idx} 'correct_answer_index' should be an integer"
    assert 0 <= quiz.correct_answer_index < len(quiz.answer_choices), f"QuizQuestion {idx} 'correct_answer_index' is out of bounds"


def test_answer_choices_length(dummy_quiz_questions):
  """
  Test that the length of answer_choices is consistent with the number of options for each quiz question.
  """
  for quiz in dummy_quiz_questions:
    assert len(quiz.answer_choices) > 0, f"Quiz question '{quiz.question}' has no answer choices."
    assert isinstance(quiz.answer_choices, list), f"Answer choices for '{quiz.question}' is not a list."


def test_correct_answer_index(dummy_quiz_questions):
  """
  Test that the correct_answer_index corresponds to a valid answer choice for each question.
  """
  for quiz in dummy_quiz_questions:
    correct_answer = quiz.answer_choices[quiz.correct_answer_index]
    assert correct_answer, f"Quiz question '{quiz.question}' has an invalid correct answer choice."
