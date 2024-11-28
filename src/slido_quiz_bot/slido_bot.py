"""This module interacts with the Slido quiz platform to automatically answer quiz questions.

It uses Playwright to simulate user actions in a browser, such as filling in the participant's name,
waiting for quiz questions, selecting the correct answers, and submitting the responses.
"""

import os

from playwright.sync_api import sync_playwright
from rich.console import Console

from slido_quiz_bot.answer_quiz_question import answer_quiz_question
from slido_quiz_bot.quizz_question import QuizQuestion

console = Console()


def enter_participant_name(page, participant_name):
    """Enters the participant's name into the Slido quiz form and submits it.

    Args:
        page: The Playwright page object representing the browser page.
        participant_name (str): The name of the participant to enter into the form.

    Raises:
        TimeoutError: If the participant name input field or submit button is not found within the timeout.
        ValueError: If the participant name is empty.
    """
    if not participant_name:
        raise ValueError("Participant name cannot be empty.")

    try:
        # Wait for the participant name input field to be visible
        name_input_locator = page.locator('input[name="participantName"]')
        name_input_locator.wait_for(state="visible")

        # Enter the participant name into the input field
        name_input_locator.fill(participant_name)

        # Optionally click the input field (to focus), though it's not strictly necessary
        name_input_locator.click()

        # Click the submit button
        submit_button = page.locator(".btn-primary")
        submit_button.click()

    except page.TimeoutError as exc:
        raise TimeoutError("The participant name input field or the submit button could not be found.") from exc
    except Exception as e:
        raise Exception(f"An error occurred while entering the participant name: {str(e)}") from e


def wait_for_question(page, timeout=120_000):
    """Waits for the 'Send' button on the page to become visible and active.

    This indicates that the page is ready to receive user input for the question.

    Args:
        page: The Playwright page object representing the browser page.
        timeout (int): Maximum time in milliseconds to wait for the 'Send' button to appear. Default is 120,000 ms.

    Returns:
        bool: True if the 'Send' button becomes visible within the timeout period, False otherwise.

    Raises:
        TimeoutError: If the 'Send' button does not appear within the specified timeout.
        Exception: If any other unexpected error occurs.
    """
    send_button_locator = page.locator('button:text("Send")')
    try:
        send_button_locator.wait_for(state="visible", timeout=timeout)
        return True
    except page.TimeoutError as exc:
        # Raise a specific exception for timeout
        raise TimeoutError(f"'Send' button did not become visible within {timeout} ms.") from exc
    except Exception as e:
        # Handle unexpected errors
        raise Exception(f"An unexpected error occurred while waiting for the 'Send' button: {str(e)}") from e


def answer_question(page):
    """Extracts the quiz question, determines the correct answer, and submits it.

    This function waits for the quiz question to load, retrieves the question and answer choices,
    computes the correct answer (using placeholder logic), selects it, and submits the response.

    Args:
        page: The Playwright page object representing the browser page.

    Raises:
        ValueError: If no answer choices are found or if the question/answer cannot be processed.
    """
    try:
        # Wait for the quiz question to load
        question_locator = page.locator('[data-testid="poll-title"]')
        question_locator.wait_for(state="visible")
        question_text = question_locator.text_content().strip()

        if not question_text:
            raise ValueError("Question text could not be retrieved.")

        console.log(f"[bold yellow]Question:[/bold yellow] {question_text}")

        # Extract all possible answer choices
        answer_locator = page.locator(".poll-question-options .MuiFormControlLabel-label")
        answer_choices = answer_locator.all_text_contents()

        if not answer_choices:
            raise ValueError("No answer choices found for the quiz.")

        # Compute the correct answer
        quiz_question = QuizQuestion(
            question=question_text,
            answer_choices=answer_choices,
            correct_answer_index=None,
        )
        correct_answer_index = answer_quiz_question(quiz_question)
        correct_answer = quiz_question.answer_choices[correct_answer_index]
        console.log(f"[bold green]Answer:[/bold green] {correct_answer}")

        # Select the correct answer
        correct_answer_locator = page.locator(f"input[type='radio'][aria-label='{correct_answer}']")
        correct_answer_locator.click()

        # Submit the answer
        send_button = page.locator('button.poll__btn-submit.btn-primary.doubleScalePulse[type="button"]')
        send_button.click()

    except ValueError as ve:
        console.log(f"[bold red]Error:[/bold red] {ve}")
        raise
    except Exception as e:
        console.log(f"[bold red]Unexpected Error:[/bold red] {e}")
        raise


def is_last_question(page):
    """Checks if the current question is the last question based on the question counter.

    Args:
        page: The Playwright page object representing the browser page.

    Returns:
        bool: True if the current question is the last question, False otherwise.

    Raises:
        ValueError: If the question counter cannot be parsed or is invalid.
    """
    try:
        # Get the question counter text
        question_counter_text = page.locator("[data-testid='question-counter']").text_content().strip()

        # Parse the ratio of answered questions (e.g., "1/1")
        questions_answered, total_questions = map(int, question_counter_text.split("/"))

        # Check if the current question is the last one
        return questions_answered == total_questions

    except ValueError as exc:
        raise ValueError(f"Invalid question counter format: '{question_counter_text}'. Expected 'answered/total'.") from exc


def respond_to_slido_quiz(quiz_url, participant_name):
    """Function to automatically respond to a Slido quiz.

    Args:
        quiz_url (str): The URL of the Slido quiz.
        participant_name (str): The name of the participant to enter in the quiz.
    """
    with sync_playwright() as p:
        # Enter quiz url
        is_docker_env = bool(os.getenv("HOSTNAME"))
        browser = p.chromium.launch(headless=is_docker_env)
        page = browser.new_page()
        page.goto(quiz_url)

        enter_participant_name(page, participant_name)

        with console.status("[bold blue]Waiting for a Question..."):
            is_last_question_answered = False
            while not is_last_question_answered:
                try:
                    wait_for_question(page, timeout=120_000)
                    answer_question(page)
                    is_last_question_answered = is_last_question(page)
                    page.wait_for_timeout(1000)
                except Exception as e:
                    raise ConnectionAbortedError(f"Error during quiz interaction: {e}") from e
        browser.close()
        console.log("[bold blue]Quiz Completed[/bold blue] - All questions have been answered and submitted successfully.")
