"""This module interacts with the Slido quiz platform to automatically answer quiz questions.

It uses Playwright to simulate user actions in a browser, such as filling in the participant's name,
waiting for quiz questions, selecting the correct answers, and submitting the responses.
"""

import time

from playwright.sync_api import sync_playwright

from slido_quiz_bot.answer_quiz_question import answer_quiz_question
from slido_quiz_bot.quizz_question import QuizQuestion


def respond_to_slido_quiz(quiz_url, participant_name):
    """Function to automatically respond to a Slido quiz.

    Args:
        quiz_url (str): The URL of the Slido quiz.
        participant_name (str): The name of the participant to enter in the quiz.
    """
    with sync_playwright() as p:
        # Launch the browser
        browser = p.chromium.launch(headless=False)  # Set to True for headless mode
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

        while True:
            try:
                time.sleep(1)
                can_send_answer = page.locator('button:text("Send")').is_visible()
                print(can_send_answer)
                if can_send_answer:
                    # Wait for the question to load
                    page.locator('[data-testid="poll-title"]').wait_for(state="visible")
                    # Extract the question
                    question_text = page.locator('[data-testid="poll-title"]').text_content()
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
                    # Select the correct answer (find the radio button associated with the correct answer)
                    correct_answer_locator = page.locator(f"input[type='radio'][aria-label='{correct_answer}']")
                    correct_answer_locator.click()
                    # Send the answer
                    send_button = page.locator('button.poll__btn-submit.btn-primary.doubleScalePulse[type="button"]')
                    send_button.click()
                else:
                    print("Waiting for a send button...")

            except Exception as e:
                print(f"Error or no more questions: {e}")
                raise e
                break

        page.pause()
        browser.close()

        # # Loop through questions
        # while True:
        #     try:
        #         # Select the first option as an example (you can add logic here)
        #         page.click(".answer-option:nth-child(1)")

        #         # Submit the answer
        #         page.click(".submit-button")

        #         # Wait for the next question to load
        #         page.wait_for_selector(".answer-option", timeout=5000)
        #     except Exception as e:
        #         print(f"Error or no more questions: {e}")
        #         break

        # # Close the browser
        # browser.close()


# Replace with your quiz URL and name
quiz_url = "https://qr.sli.do/4DQ6dA53AX4t99TTL434TD"
participant_name = "Your Name"
respond_to_slido_quiz(quiz_url, participant_name)
