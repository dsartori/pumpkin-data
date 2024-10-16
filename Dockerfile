FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y vim sqlite3 && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir pandas matplotlib

COPY . /app

CMD ["/bin/bash"]
