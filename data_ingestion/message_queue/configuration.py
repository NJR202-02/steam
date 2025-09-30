import os


# RabbitMQ
RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST", "127.0.0.1")
RABBITMQ_PORT = int(os.environ.get("RABBITMQ_PORT", 5672))

# Celery Worker
WORKER_USERNAME = os.environ.get("WORKER_USERNAME", "worker")
WORKER_PASSWORD = os.environ.get("WORKER_PASSWORD", "worker")