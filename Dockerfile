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

# Run the application
CMD ["bash"]
