from celery import Celery

from data_ingestion.message_queue.configuration import (
    RABBITMQ_HOST,
    RABBITMQ_PORT,
    WORKER_USERNAME,
    WORKER_PASSWORD,
)

app = Celery(
    main="worker",
    # 載入以下路徑模組註冊的 Celery 任務
    include=[
        "data_ingestion.message_queue.tasks",
    ],
    # 指定 broker 為 rabbitmq
    # pyamqp://worker:worker@127.0.0.1:5672/
    broker=f"pyamqp://{WORKER_USERNAME}:{WORKER_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/",
)

# print(f"CPU 核心數: {multiprocessing.cpu_count()}")
print("🚀 Celery 已經和 RabbitMQ 連接...")
