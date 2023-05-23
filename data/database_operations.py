import pandas as pd
import sqlite3
import os
import json


def csv_to_table(path: str, database: str, table: str):
  with open(path) as file:
    df = pd.read_csv(file)
  with sqlite3.connect(database) as conn:
    df.to_sql(table, conn, index=False)


def load_csv_from_database(database: str, table: str):
  with sqlite3.connect(database) as conn:
    query = f"SELECT * FROM {table}"
    df = pd.read_sql_query(query, conn)
    return df
  

def json_to_table(path: str, database: str, table: str, columns: list[str]):
  with open(path) as file:
    data = json.load(file)
  df = pd.DataFrame(columns=columns, data=data.items())
  with sqlite3.connect(database) as conn:
    df.to_sql(table, conn, index=False)

  
def load_json_from_database(database: str, table: str):
  with sqlite3.connect(database) as conn:
    cursor = conn.cursor()
    query = f"SELECT * FROM {table}"
    res = dict(cursor.execute(query).fetchall())
  return res


def load_all_data(folder: str, database_name: str):
  database_path = folder + '/' + database_name
  if os.path.exists(database_path):
    os.remove(database_path)
  
  # csv to sql table
  data_csv, table_name = f'{folder}/data.csv', f'{folder}_data'
  csv_to_table(data_csv, database_path, table_name)
  data = load_csv_from_database(database_path, table_name)
  
  # json to sql table
  years_json, table_name, columns = f'{folder}/years.json', f'{folder}_years', ['year', 'year_string']
  json_to_table(f'{years_json}', database_path, table_name, columns)
  years = load_json_from_database(database_path, table_name)

  series_json, table_name, columns = f'{folder}/series.json', f'{folder}_series', ['series', 'description']
  json_to_table(f'{series_json}', database_path, table_name, columns)
  series = load_json_from_database(database_path, table_name)

  countries_json, table_name, columns = f'{folder}/countries.json', f'{folder}_countries', ['country_code', 'country']
  json_to_table(f'{countries_json}', database_path, table_name, columns)
  countries = load_json_from_database(database_path, table_name)

  return data, years, series, countries

  
  
if __name__ == "__main__":
  load_all_data('preprocessed', 'world_data.db')