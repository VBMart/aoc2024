#FROM python:3.9.19-bullseye
FROM pypy:3

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY . requirements.txt /app/
RUN pip install -r requirements.txt

STOPSIGNAL SIGINT
CMD python main.py
