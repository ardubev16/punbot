FROM python:3.12.2-alpine3.19

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY punbot ./punbot

CMD [ "python3", "main.py" ]
