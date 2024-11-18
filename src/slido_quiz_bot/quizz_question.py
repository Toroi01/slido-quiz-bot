from dataclasses import dataclass


@dataclass(frozen=True)
class QuizQuestion:
  """
  A data class representing a multiple-choice quiz question with answer choices.

  Attributes:
      question (str): The quiz question text.
      answer_choices (list[str]): A list of possible answer choices.
      correct_answer_index (int): The index of the correct answer in the list of choices.
  """

  question: str
  answer_choices: list[str]
  correct_answer_index: int
