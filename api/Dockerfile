# Stage 1: Build environment
FROM python:3.12-slim AS builder

COPY ./requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Stage 2: Production Environment
FROM python:3.12-slim

COPY --from=builder /usr/local /usr/local

WORKDIR /app
COPY . .

ENV PYTHONPATH=/app
ENV IS_DOCKER_CONTAINER=true

EXPOSE 8000

CMD ["python", "main.py", "run"]