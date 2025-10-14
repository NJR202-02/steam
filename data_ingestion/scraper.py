import os
import time
from datetime import datetime, timezone

import re
import json
import pandas as pd

import requests
from requests.exceptions import HTTPError

from data_ingestion.database.schema import (
    game_check_table,
    game_information_table,
    game_genre_table,
    game_review_summary_table,
    game_review_detail_table,
)

from data_ingestion.database.upload import insert_data, insert_data_sqlalchemy, upsert_data_sqlalchemy


HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
}


def get_application_list() -> json:
    """
    """
    
    URL = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"

    response = requests.get(URL, headers=HEADERS)

    print(f"HTTP status code: {response.status_code}")

    application_list = response.json()["applist"]["apps"]

    # print(f"Number of applications: {len(application_list)}")

    return application_list


def get_game_information(application_id: str, exist: bool = False):
    """
    game_check
    game_information
    game_genre
    """
    print(f"Processing: {application_id}")

    url = f"https://store.steampowered.com/api/appdetails?appids={application_id}&cc=TW"

    while True:
        try:
            response = requests.get(url, headers=HEADERS)
            response.raise_for_status()
            print(f"HTTP status code: {response.status_code}")
            break
        except HTTPError as http_err:
            status_code = http_err.response.status_code if http_err.response else None
            if status_code == 429:
                print(f"Too many requests")
            else:
                print(f"HTTP error occurred: {http_err} - status code: {status_code}")
            time.sleep(5)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            time.sleep(5)
    
    if not response.json()[f"{application_id}"]["success"]:
        is_game = 0
    elif not response.json()[f"{application_id}"]["data"]["type"] == "game":
        is_game = 0
    else:
        is_game = 1

        get_game_review(application_id, exist=False)
        
        game_detail = response.json()[f"{application_id}"]["data"]

        if game_detail.get("supported_languages") is None:
            supported_languages = None
        else:
            supported_languages = game_detail.get("supported_languages").replace("<strong>*</strong>", "")

        if game_detail.get("developers") is None:
            developers = None
        else:
            developers = "|".join(game_detail.get("developers"))

        if game_detail.get("publishers") is None:
            publishers = None
        else:
            publishers = "|".join(game_detail.get("publishers"))

        if game_detail.get("price_overview") is None:
            # initial_price = None
            # final_price = None
            # discount_percent = None
            # initial_formatted = None
            final_formatted = None
        else:
            # initial_price = game_detail.get("price_overview").get("initial")
            # final_price = game_detail.get("price_overview").get("final")
            # discount_percent = game_detail.get("price_overview").get("discount_percent")
            # initial_formatted = game_detail.get("price_overview").get("initial_formatted")
            final_formatted = game_detail.get("price_overview").get("final_formatted")
        
        pattern = r"['A-Z']"

        try:
            if game_detail.get("release_date").get("date") == "":
                release_date = None
            elif game_detail.get("release_date").get("date") == "Coming soon":
                release_date = None
            else:
                if re.match(pattern, game_detail.get("release_date").get("date")[0]):
                    release_date = datetime.strptime(game_detail.get("release_date").get("date"), "%b %d, %Y")
                else:
                    release_date = datetime.strptime(game_detail.get("release_date").get("date"), "%d %b, %Y")
        except Exception as e:
            release_date = None
            print(f"An unexpected error occurred: {e}")
        
        game_information = {
            "app_id": application_id,
            
            "steam_app_id": game_detail.get("steam_appid"),
                
            "name": game_detail.get("name"),

            # "type": game_detail.get("type"),

            "required_age": game_detail.get("required_age"),

            "is_free": game_detail.get("is_free"),

            "supported_languages": supported_languages,

            "header_image": game_detail.get("header_image", None),

            "developers": developers,
            "publishers": publishers,
                
            # "initial_price": initial_price,
            # "final_price": final_price,
            # "discount_percent": discount_percent,
            # "initial_formatted": initial_formatted,
            "final_formatted": final_formatted,

            "release_date": release_date,
        }

        upsert_data_sqlalchemy(table_object=game_information_table, data=[game_information])


        game_genre_list = []

        if game_detail.get("genres") is None:
            game_genre = None
        else:
            for item in game_detail.get("genres"):
                game_genre_dict = {
                    "app_id": application_id,
                    "genre_id": item.get("id"),
                    "genre_description": item.get("description"),
                }
                game_genre_list.append(game_genre_dict)
        
        upsert_data_sqlalchemy(table_object=game_genre_table, data=game_genre_list)
    

    game_check = {
        "app_id": application_id,
        "is_game": is_game,
    }

    upsert_data_sqlalchemy(table_object=game_check_table, data=[game_check])

    time.sleep(1)

    return None


def get_game_review(application_id: str, filtered_language: str = "tchinese", exist: bool = False):
    """
    game_review_summary
    game_review_detail
    """
    print(f"Processing: {application_id}")

    game_review_detail_list = []

    url = f"https://store.steampowered.com/appreviews/{application_id}?"

    if exist:
        PAGE_LIMIT = 5

    page = 1

    while True:
        print(f"Page: {page}")

        if page == 1:
            next_page_cursor = "*"
        else:
            next_page_cursor = next_page_cursor

        payload = {
            "json": 1,
            "filter": "recent",
            "language": filtered_language,
            "cursor": next_page_cursor,
            "day_range": 30,
            "num_per_page": 100,
        }

        while True:
            try:
                response = requests.get(url, params=payload, headers=HEADERS)
                response.raise_for_status()
                print(f"HTTP status code: {response.status_code}")
                break
            except HTTPError as http_err:
                status_code = http_err.response.status_code if http_err.response else None
                if status_code == 429:
                    print(f"Too many requests")
                else:
                    print(f"HTTP error occurred: {http_err} - status code: {status_code}")
                time.sleep(5)
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                time.sleep(5)

        if page == 1:
            game_review_summary_dict = {
                "app_id": application_id,
                "review_score": response.json()["query_summary"]["review_score"],
                "review_score_desc": response.json()["query_summary"]["review_score_desc"],
                "total_positive": response.json()["query_summary"]["total_positive"],
                "total_negative": response.json()["query_summary"]["total_negative"],
                "total_reviews": response.json()["query_summary"]["total_reviews"],
                "capture_date": datetime.now(timezone.utc),
            }

            upsert_data_sqlalchemy(table_object=game_review_summary_table, data=[game_review_summary_dict])

        for i in range(response.json()["query_summary"]["num_reviews"]):

            review_data = response.json()["reviews"][i]
            
            game_review_detail_dict = {
                "recommendation_id": review_data["recommendationid"],
                "app_id": application_id,
                
                "author_id": review_data["author"]["steamid"],
                "num_games_owned": review_data["author"]["num_games_owned"],
                "num_reviews": review_data["author"]["num_reviews"],
                "playtime_forever": review_data["author"]["playtime_forever"],
                "playtime_last_two_weeks": review_data["author"]["playtime_last_two_weeks"],
                "playtime_at_review": review_data.get("author").get("playtime_at_review", None),
                "last_played": datetime.fromtimestamp(review_data["author"]["last_played"]),
                
                "language": review_data["language"],
                "review": (review_data["review"]).strip(),
                "timestamp_created": datetime.fromtimestamp(review_data["timestamp_created"]),
                "timestamp_updated": datetime.fromtimestamp(review_data["timestamp_updated"]),
                "voted_up": review_data["voted_up"],
                "votes_up": review_data["votes_up"],
                "votes_funny": review_data["votes_funny"],
                "weighted_vote_score": review_data["weighted_vote_score"],
                "comment_count": review_data["comment_count"],
                "steam_purchase": review_data["steam_purchase"],
                "received_for_free": review_data["received_for_free"],
                "written_during_early_access": review_data["written_during_early_access"],
                # "primarily_steam_deck": review_data["primarily_steam_deck"],
            }

            game_review_detail_list.append(game_review_detail_dict)

        upsert_data_sqlalchemy(table_object=game_review_detail_table, data=game_review_detail_list)

        if exist and page == PAGE_LIMIT:
            break
        elif response.json()["query_summary"]["num_reviews"] < 100:
            print(response.json()["query_summary"]["num_reviews"])
            break

        next_page_cursor = response.json()["cursor"]

        page = page + 1
        
        time.sleep(1)

    return None


if __name__ == "__main__":

    application_list = get_application_list()

    print(len(application_list))

    # k = 100

    for item in application_list:
        application_id = item.get("appid")
        get_game_information(application_id)
        # get_game_review(application_id)