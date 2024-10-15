FROM python:3.9-slim

WORKDIR /app

RUN pip install --no-cache-dir pandas matplotlib

COPY . /app

CMD ["/bin/bash"]
