from dataclasses import dataclass


@dataclass(frozen=True)
class QuizQuestion:
  question: str
  answer_choices: list[str]
  correct_answer_index: int


# Creating multiple QuizQuestion instances
quiz_questions = [
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
    answer_choices=[
      "Atlantic Ocean",
      "Indian Ocean",
      "Arctic Ocean",
      "Pacific Ocean",
    ],
    correct_answer_index=3,  # Pacific Ocean is the correct answer
  ),
  QuizQuestion(
    question="Who wrote 'Romeo and Juliet'?",
    answer_choices=[
      "Charles Dickens",
      "Jane Austen",
      "Mark Twain",
      "William Shakespeare",
    ],
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
    answer_choices=[
      "Vincent Van Gogh",
      "Pablo Picasso",
      "Leonardo da Vinci",
    ],
    correct_answer_index=2,  # Leonardo da Vinci is the correct answer
  ),
]
