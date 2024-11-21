# Build the image:
# docker build -t slido-quiz-bot .

# Run the image:
# docker run -it --env-file .env slido-quiz-bot -u "<SLIDO URL>" -n "<USER NAME>"
# Example:
# docker run -it --env-file .env slido-quiz-bot -u "https://app.sli.do/event/4DQ6dA53AX4t99TTL434TD" -n "Alan Turing"

# Use an official Python runtime as a parent image
FROM mcr.microsoft.com/playwright/python:v1.48.0-noble

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy only requirements to cache them in docker layer
COPY pyproject.toml poetry.lock* /app/

# Copy project
COPY . /app

# Project initialization:
RUN poetry config virtualenvs.create false \
&& poetry install --no-interaction --only main

# Install the browser
RUN poetry run playwright install

# Entry point to run the bot with parameters passed during container run
ENTRYPOINT ["poetry", "run", "slido-quiz-bot"]

# Command to pass arguments dynamically at runtime
CMD ["-u", "<slido_url>", "-n", "<participant_name>"]
