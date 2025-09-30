import time
from data_ingestion.message_queue.worker import app

# from data_ingestion.scraper import get_application_list as _get_application_list
from data_ingestion.scraper import get_game_information as _get_game_information
from data_ingestion.scraper import get_game_review as _get_game_review


# @app.task()
# def get_application_list_celery(**kwargs):
#     """
#     """
#     _get_application_list()
#     return


@app.task()
def get_game_information_celery(application_list: list, **kwargs):
    """
    """
    print(f"Start")
    for item in application_list:
        application_id = item.get("appid")
        _get_game_information(application_id)
        time.sleep(300)


@app.task()
def get_game_review_celery(application_id: str, **kwargs):
    """
    """
    _get_game_review(application_id)