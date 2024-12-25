#FROM python:3.9.19-bullseye
FROM pypy:3

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Update the package list, install Graphviz and dependencies
RUN apt-get update && apt-get install -y \
    graphviz \
    libgraphviz-dev \
    graphviz-dev \
    pkg-config \
    python3-dev \
    xdg-utils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Verify that the Graphviz binary is installed and on PATH
RUN which dot

WORKDIR /app

COPY . requirements.txt /app/
RUN pip install -r requirements.txt

STOPSIGNAL SIGINT
CMD python main.py
