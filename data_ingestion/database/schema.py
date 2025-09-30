import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy import MetaData, Table, Column
from sqlalchemy import Boolean, Float, String, Integer, Text, DECIMAL, DATETIME
from sqlalchemy.dialects.mysql import LONGTEXT

from data_ingestion.database.configuration import (
    MYSQL_USERNAME,
    MYSQL_PASSWORD,
    MYSQL_HOST,
    MYSQL_PORT,
    MYSQL_DATABASE,
)


# Create metadata
metadata = MetaData()

game_check_table = Table(
    "game_check",
    metadata,
    Column("app_id", String(8), primary_key=True, comment="application_id"),
    Column("is_game", Integer, nullable=True, default=0),
)

game_information_table = Table(
    "game_information",
    metadata,
    Column("app_id", String(8), primary_key=True, comment="outer_application_id"),
    Column("steam_app_id", String(8), nullable=False, comment="inner_application_id"),

    Column("name", String(100), nullable=False, comment="application_name"),
    Column("required_age", Integer, nullable=False, comment=""),
    Column("is_free", Integer, nullable=False, comment=""),
    Column("supported_languages", LONGTEXT, nullable=False, comment=""),
    Column("header_image", String(255), nullable=False, comment=""),
    Column("developers", String(100), nullable=False, comment=""),
    Column("publishers", String(100), nullable=False, comment=""),
    Column("final_formatted", String(8), nullable=True, default=None, comment=""),
    Column("release_date", DATETIME, nullable=False, comment=""),
)

game_genre_table = Table(
    "game_genre",
    metadata,
    Column("app_id", String(8), primary_key=True, comment="application_id"),
    Column("genre_id", Integer, primary_key=True),
    Column("genre_description", String(32), nullable=False),
)

game_review_summary_table = Table(
    "game_review_summary",
    metadata,
    Column("app_id", String(8), primary_key=True, comment="application_id"),
    Column("review_score", Float, nullable=False),
    Column("review_score_desc", String(255), nullable=False),
    Column("total_positive", Integer, nullable=True, default=-1),
    Column("total_negative", Integer, nullable=True, default=-1),
    Column("total_reviews", Integer, nullable=True, default=-1),
    Column("capture_date", DATETIME, nullable=False),
)

game_review_detail_table = Table(
    "game_review_detail",
    metadata,
    Column("recommendation_id", String(32), primary_key=True, comment="recommendation_id"),
    Column("app_id", String(8), primary_key=True, comment="application_id"),
    Column("author_id", String(32), primary_key=True, comment="author_id"),
    Column("num_games_owned", Integer, nullable=False, default=0, comment=""),
    Column("num_reviews", Integer, nullable=False, default=0, comment=""),
    Column("playtime_forever", Integer, nullable=False, default=0, comment=""),
    Column("playtime_last_two_weeks", Integer, nullable=False, default=0, comment=""),
    Column("playtime_at_review", Integer, nullable=False, default=0, comment=""),
    Column("last_played", DATETIME, nullable=True, default=None, comment=""),
    Column("language", LONGTEXT, nullable=True, comment=""),
    Column("review", LONGTEXT, nullable=False, comment=""),
    Column("timestamp_created", DATETIME, nullable=False, comment=""),
    Column("timestamp_updated", DATETIME, nullable=False,  comment=""),
    Column("voted_up", Boolean, nullable=False, comment=""),
    Column("votes_up", Integer, nullable=False,  comment=""),
    Column("votes_funny", Integer, nullable=False,  comment=""),
    Column("weighted_vote_score", Float, nullable=False,  comment=""),
    Column("comment_count", Integer, nullable=False,  comment=""),
    Column("steam_purchase", Boolean, nullable=False,  comment=""),
    Column("received_for_free", Boolean, nullable=False,  comment=""),
    Column("written_during_early_access", Boolean, nullable=False,  comment=""),
)



if __name__ == "__main__":
    print(MYSQL_USERNAME)
    print(MYSQL_PASSWORD)
    print(MYSQL_HOST)
    print(MYSQL_PORT)
    print(MYSQL_DATABASE)