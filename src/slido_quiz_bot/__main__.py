"""This is the main entry point for the Slido quiz bot.

It accepts a Slido quiz URL and a participant's name through the command line
and simulates answering the quiz on Slido using the `respond_to_slido_quiz`
function.

Usage:
    python slido_bot.py -u <slido_url> -n <participant_name>
    poetry run slido-quiz-bot -u <slido_url> -n <participant_name>
    slido-quiz-bot -u <slido_url> -n <participant_name>
"""

import argparse

from slido_quiz_bot.slido_bot import respond_to_slido_quiz


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
