
FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install "poetry==1.6.1"

COPY poetry.lock pyproject.toml /app/


RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

COPY . /app
RUN poetry install --no-interaction --no-ansi

ENV PATH_TO_DATA="/app/data/bookstore_v4.db"
CMD exec streamlit run app/Chat.py --server.headless true --server.port 8081