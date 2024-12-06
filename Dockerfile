FROM python:3.9.19-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY . requirements.txt /app/
RUN pip install -r requirements.txt

STOPSIGNAL SIGINT
CMD python main.py
