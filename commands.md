docker build -t slido-quiz-bot .

docker run -it --env-file .env slido-quiz-bot

poetry run slido-quiz-bot -u "https://app.sli.do/event/4DQ6dA53AX4t99TTL434TD"
