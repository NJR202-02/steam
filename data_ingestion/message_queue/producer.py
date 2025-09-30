import math

from data_ingestion.scraper import get_application_list

from data_ingestion.message_queue.tasks import(
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

for batch in zip(start, end):
    print(f"Send tasks{batch}")
    get_game_information_celery.delay(application_list=application_list[batch[0]:batch[1]])
