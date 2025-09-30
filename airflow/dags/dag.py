from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator

from data_ingestion.scraper import (
    get_application_list,
    get_game_information,
    get_game_review,
)

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


def trigger_scraper(application_list):
    get_game_information_celery.delay(application_list)


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

    for batch in zip(start, end):
        task = PythonOperator(
            task_id=f"scrape_{}",
            python_callable=trigger_scraper,
            op_args=[],
        )
        batch_tasks.append(task)


    

for batch in zip(start, end):
    print(f"Send tasks{batch}")
    get_game_information_celery.delay(application_list=application_list[batch[0]:batch[1]])


    # get_application_list_op = PythonOperator(
    #     task_id="get_application_list",
    #     python_callable=get_application_list,
    # )
    
    # get_game_information_op = PythonOperator(
    #     task_id="get_game_information",
    #     python_callable=get_game_information,
    #     # op_args=[],
    # )

    # get_game_review_op = PythonOperator(
    #     task_id="get_game_review",
    #     python_callable=get_game_review,
    # )

    end_task = DummyOperator(
        task_id="end"
    )

    start_task >> step_1_task >> step_2_task >> end_task