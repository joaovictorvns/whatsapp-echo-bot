FROM python:3.13.0-slim-bookworm

WORKDIR /whatsapp-echo-bot

COPY pyproject.toml poetry.lock ./
COPY whatsapp_echo_bot ./whatsapp_echo_bot

RUN pip install poetry==1.8.3
RUN poetry install --only main

CMD ["poetry", "run", "gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "whatsapp_echo_bot:create_app()"]
