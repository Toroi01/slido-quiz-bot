# Slido Quiz Bot

A bot that automatically completes Slido quizzes by generating answers to all questions using Gemini AI.

## Demo Video

[Watch on YouTube](https://youtu.be/eTKHASi9FzQ)

## Features
- Automatically joins and answers Slido quiz questions.
- Configurable via environment variables for flexibility and security.
- Supports custom names and quiz URLs.
- Lightweight and containerized for easy deployment.

## Requirements

- [Python 3.10](https://www.python.org/downloads/release/python-3100/) or higher
- [Docker](https://www.docker.com/products/docker-desktop) (For containerized use)
- [Poetry](https://python-poetry.org/) (For local use)
- Slido quiz URL and participant name

## Installation

### Local Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/Toroi01/slido-quiz-bot.git
   cd slido-quiz-bot
   ```
2. Install dependencies and set up a virtual environment using Poetry:
   ```bash
   poetry install
   ```
3. Install Playwright and its required dependencies:
   ```bash
   poetry run playwright install
   ```
### Docker Setup
1. Pull the Docker image:
   ```bash
   docker pull cbot/slido-quiz-bot:latest
   ```
## Usage

### Local Usage

1. **Set up your environment:**

   You need to define the `GOOGLE_API_KEY` in your local environment to run the bot.

   - **On Windows:**
     1. Open Command Prompt or PowerShell.
     2. Set the environment variable:
        ```powershell
        set GOOGLE_API_KEY=<your_google_api_key>
        ```

   - **On Unix/Linux/macOS:**
     1. Open Terminal.
     2. Set the environment variable:
        ```bash
        export GOOGLE_API_KEY=<your_google_api_key>
        ```

2. **Run the bot:**

   After setting the environment variable, run the bot with the following command, specifying the required inputs:

   ```bash
   poetry run slido-quiz-bot -u "<SLIDO_URL>" -n "<USER_NAME>"
   ```
    > **Note:** You can easily obtain the SLIDO_URL by scanning the QR code using this website: [https://qrscanner.net/](https://qrscanner.net/)

### Docker Usage

To run the bot with the required environment variables and inputs, use one of the following methods:

### Option 1: Pass the environment variable directly in the command
```bash
docker run -e GOOGLE_API_KEY=<your_google_api_key> cbot/slido-quiz-bot:latest -u "<SLIDO_URL>" -n "<USER_NAME>"
```
### Option 2: Pass the environment variable using a `.env` file
Alternatively, you can define your environment variables in a `.env` file and load them into the container by using the `--env-file` option:
1. Create a `.env` file with the following content:
    ```bash
    GOOGLE_API_KEY=<your_google_api_key>
2. Run the bot with the `.env` file:
    ```bash
    docker run --env-file .env cbot/slido-quiz-bot:latest -u "<SLIDO_URL>" -n "<USER_NAME>"
    ```
