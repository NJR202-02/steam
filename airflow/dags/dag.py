import math
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator

from data_ingestion.scraper import get_application_list

from data_ingestion.message_queue.tasks import (
    get_game_information_celery,
    get_game_review_celery,
)

def split(total_count, k: int = 30):
    base = math.ceil(total_count / k)

    start = []
    end = []

    for i in range(k):

        start.append(i * base)

        if i == (k - 1):
            end.append(total_count)
        else:
            end.append(i * base + base)
    
    return start, end

application_list = get_application_list()

start, end = split(len(application_list))

def trigger_scraper(batch):
    print(batch[0])
    print(batch[1])

    for item in application_list[batch[0]:batch[1]]:
        application_id = item.get("appid")
        print(application_id)
        get_game_information_celery.delay(application_id)


default_arguments = {
    "owner": "NJR202-02-22",

    "retries": 1,
    "retry_delay": timedelta(minutes=1),
    "depends_on_past": False,
    # "email": [""],
    # "email_on_failure": False,
    # "email_on_retry": False,
}


with DAG(
    dag_id="dag",
    default_args=default_arguments,
    description="",
    schedule_interval="0 * * * *",  # 每小時執行
    start_date=datetime(2025, 9, 30),
    catchup=False,
    tags=["steam"],
) as dag:
    
    start_task = DummyOperator(
        task_id="start"
    )

    batch_tasks = []

    for index, batch in enumerate(zip(start, end)):

        task = PythonOperator(
            task_id=f"scraper_{index}",
            python_callable=trigger_scraper,
            op_args=[batch],
        )

        batch_tasks.append(task)

    end_task = DummyOperator(
        task_id="end"
    )

    start_task >> batch_tasks >> end_task