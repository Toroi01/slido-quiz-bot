"""This module interacts with the Slido quiz platform to automatically answer quiz questions.

It uses Playwright to simulate user actions in a browser, such as filling in the participant's name,
waiting for quiz questions, selecting the correct answers, and submitting the responses.
"""
# TODO: Refactor breaking the huge main logic into small pieces.

import argparse
import os
import time

from playwright.sync_api import sync_playwright
from rich.console import Console

from slido_quiz_bot.answer_quiz_question import answer_quiz_question
from slido_quiz_bot.quizz_question import QuizQuestion

console = Console()


def is_leaderboard_visible(page):
    """Check if an element with class 'quiz-statistics' is visible on the page."""
    try:
        leaderboard_locator = page.locator(".quiz-statistics")  # Locate elements with the class
        return leaderboard_locator.is_visible(timeout=3000)  # Adjust timeout as needed
    except Exception as e:
        print(f"Leaderboard not detected: {e}")
        return False


def respond_to_slido_quiz(quiz_url, participant_name):
    """Function to automatically respond to a Slido quiz.

    Args:
        quiz_url (str): The URL of the Slido quiz.
        participant_name (str): The name of the participant to enter in the quiz.
    """
    with sync_playwright() as p:
        # Launch the browser
        is_docker_env = bool(os.getenv("HOSTNAME"))
        browser = p.chromium.launch(headless=is_docker_env)  # Set to True for headless mode
        page = browser.new_page()

        # Open the Slido quiz URL
        page.goto(quiz_url)

        # Wait for the name input field to appear
        page.wait_for_selector('input[name="participantName"]')

        # Fill the name input field
        page.fill('input[name="participantName"]', participant_name)

        # Agree to the name usage by enabling the button
        page.click('input[name="participantName"]')  # Ensure focus on the input
        page.click(".btn-primary")  # Click the "Join" button
        with console.status("[bold blue]Waiting for the Send button to become active..."):
            while True:
                try:
                    time.sleep(1)
                    if is_leaderboard_visible(page):
                        console.log("[bold blue] Leaderboard detected. Finishing the program...")
                        break
                    send_button_locator = page.locator('button:text("Send")')
                    can_send_answer = send_button_locator.is_visible(timeout=5000)
                    if can_send_answer:
                        # Wait for the question to load
                        page.locator('[data-testid="poll-title"]').wait_for(state="visible")
                        # Extract the question
                        question_text = page.locator('[data-testid="poll-title"]').text_content()
                        console.log(f"[bold yellow]\nQuestion:[/bold yellow] {question_text}")
                        # Extract all possible answer texts
                        answers = page.locator(".poll-question-options .MuiFormControlLabel-label")
                        # Use the `all_text_contents` method to get all answer texts
                        answer_choices = answers.all_text_contents()
                        # Compute the correct answer
                        quiz_question = QuizQuestion(
                            question=question_text,
                            answer_choices=answer_choices,
                            correct_answer_index=None,
                        )
                        correct_answer_index = answer_quiz_question(quiz_question)
                        correct_answer = quiz_question.answer_choices[correct_answer_index]
                        console.log(f"[bold green]Answer:[/bold green] {correct_answer}")
                        # Select the correct answer (find the radio button associated with the correct answer)
                        correct_answer_locator = page.locator(f"input[type='radio'][aria-label='{correct_answer}']")
                        correct_answer_locator.click()
                        # Send the answer
                        send_button = page.locator('button.poll__btn-submit.btn-primary.doubleScalePulse[type="button"]')
                        send_button.click()

                except Exception as e:
                    raise ConnectionAbortedError(f"Error during quiz interaction: {e}") from e
        browser.close()


# Define the CLI entry point
def main():
    """Main function to handle the Slido quiz participation.

    This function sets up an argument parser to accept a Slido quiz URL and
    participant name, then calls the `respond_to_slido_quiz` function to
    simulate answering the quiz.

    Arguments:
        - slio_url (str): The URL of the Slido quiz.
        - participant_name (str): The name of the participant (defaults to "Alan Turing").

    Usage:
        python slido_bot.py -u <slido_url> -n <participant_name>
        poetry run slido-quiz-bot -u <slido_url> -n <participant_name>
        slido-quiz-bot -u <slido_url> -n <participant_name>
    """
    # Create an argument parser
    parser = argparse.ArgumentParser(description="Respond to a Slido quiz.")
    parser.add_argument("-u", "--slio_url", type=str, required=True, help="The Slido quiz URL.")
    parser.add_argument("-n", "--participant_name", type=str, default="Alan Turing", help="The participant name to answer the quiz.")

    # Parse the arguments
    args = parser.parse_args()

    # Call the function with parsed arguments
    respond_to_slido_quiz(args.slio_url, args.participant_name)


if __name__ == "__main__":
    main()
