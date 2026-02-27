FROM python:3.13.1-alpine3.19

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:0.10.7 /uv /bin/uv
COPY pyproject.toml .
RUN uv pip install --system -r pyproject.toml

COPY main.py .
COPY punbot ./punbot

CMD [ "python3", "main.py" ]
