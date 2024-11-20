"""Tests for the `answer_quiz_question` function."""

from unittest.mock import MagicMock, patch

import pytest

from slido_quiz_bot.answer_quiz_question import answer_quiz_question, format_prompt


def test_format_prompt(dummy_quiz_questions):
    """Test the formatting of quiz question prompts."""
    quiz_question = dummy_quiz_questions[0]  # Use the first question
    expected_output = (
        "Question: What is the capital of France?\nChoices:\n0. Berlin\n1. Madrid\n2. Paris\n3. Rome\nChoose the best answer (provide the number):"
    )
    assert format_prompt(quiz_question) == expected_output


@patch("slido_quiz_bot.answer_quiz_question.genai.GenerativeModel")
def test_answer_quiz_question(mock_model_class, dummy_quiz_questions):
    """Test the quiz question answering function with mocked AI model."""
    quiz_question = dummy_quiz_questions[1]  # Use the second question

    # Mock the model and its behavior
    mock_model = MagicMock()
    mock_model.generate_content.return_value.int = quiz_question.correct_answer_index
    mock_model_class.return_value = mock_model

    # Call the function
    result = answer_quiz_question(quiz_question)

    # Validate the interactions and result
    assert result == quiz_question.correct_answer_index
    mock_model.generate_content.assert_called_once_with(
        format_prompt(quiz_question),
        generation_config=mock_model.generate_content.call_args[1]["generation_config"],
    )


def test_answer_quiz_question_invalid_response(dummy_quiz_questions):
    """Test error handling when the model returns an invalid response."""
    quiz_question = dummy_quiz_questions[2]  # Use the third question

    with patch("slido_quiz_bot.answer_quiz_question.genai.GenerativeModel") as mock_model_class:
        mock_model = MagicMock()
        mock_model.generate_content.return_value.text = "invalid"
        mock_model_class.return_value = mock_model

        with pytest.raises(ValueError, match="The model's response could not be converted to an integer."):
            answer_quiz_question(quiz_question)


def test_answer_quiz_question_model_error(dummy_quiz_questions):
    """Test error handling when the model raises an exception."""
    quiz_question = dummy_quiz_questions[3]  # Use the fourth question

    with patch("slido_quiz_bot.answer_quiz_question.genai.GenerativeModel") as mock_model_class:
        mock_model = MagicMock()
        mock_model.generate_content.side_effect = RuntimeError("Model failure")
        mock_model_class.return_value = mock_model

        with pytest.raises(RuntimeError, match="An error occurred while generating the answer: Model failure"):
            answer_quiz_question(quiz_question)
