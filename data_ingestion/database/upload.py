import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.exc import IntegrityError

from data_ingestion.database.configuration import (
    MYSQL_USERNAME,
    MYSQL_PASSWORD,
    MYSQL_HOST,
    MYSQL_PORT,
    MYSQL_DATABASE,
)

# Create metadata
metadata = MetaData()


def insert_data(
        table_name: str,
        dataframe: pd.DataFrame,
        if_exists_mode: str = "append"
    ) -> None:
    mysql_address = f"mysql+pymysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
    engine = create_engine(mysql_address)

    with engine.connect() as connection:
        dataframe.to_sql(
            table_name,
            con=connection,
            if_exists=if_exists_mode,
            index=False
        )
    
    print(f"Finish to Insert data")

def insert_data_sqlalchemy(
        table_object: Table,
        data: list[dict],
    ) -> None:
    mysql_address = f"mysql+pymysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
    engine = create_engine(mysql_address)

    # Create datatable (if it doesn't exist)
    metadata.create_all(engine, tables=[table_object])

    with engine.begin() as connection:
        for row in data:
            try:
                insert_statement = insert(table_object).values(**row)
                connection.execute(insert_statement)
            except IntegrityError as e:
                print(f"Insert failed due to IntegrityError (可能是主鍵重複): {e.orig}")
                continue

    print(f"Finish to Insert data")


def upsert_data_sqlalchemy(
        table_object: Table,
        data: list[dict],
    ) -> None:
    mysql_address = f"mysql+pymysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
    engine = create_engine(mysql_address)

    # Create datatable (if it doesn't exist)
    metadata.create_all(engine, tables=[table_object])

    with engine.begin() as connection:
        for row in data:
            insert_statement = insert(table_object).values(**row)
            update_dict = {
                column.name: insert_statement.inserted[column.name]
                for column in table_object.columns
            }
            upsert_statement = insert_statement.on_duplicate_key_update(**update_dict)
            connection.execute(upsert_statement)

    print(f"Finish to Upsert data")


def read_data(table_name: str):

    mysql_address = f"mysql+pymysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
    engine = create_engine(mysql_address)

    dataframe = pd.read_sql(f"SELECT * FROM {table_name}", con=engine)

    return dataframe


if __name__ == "__main__":
    print(MYSQL_USERNAME)
    print(MYSQL_PASSWORD)
    print(MYSQL_HOST)
    print(MYSQL_PORT)
    print(MYSQL_DATABASE)

