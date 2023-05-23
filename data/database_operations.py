import pandas as pd
import sqlite3
import os
import json


def csv_to_table(path: str, database: str, table: str):
  with open(path) as file:
    df = pd.read_csv(file)
    df['year'] = df['year'].apply(lambda x: str(int(x)))
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


def save_all_data_to_db(folder: str, database_name: str):
  database_path = folder + '/' + database_name
  if os.path.exists(database_path):
    os.remove(database_path)

  # csv to sql table
  data_csv, table_name = f'{folder}/data.csv', f'{folder}_data'
  csv_to_table(data_csv, database_path, table_name)

  # json to sql table
  years_json, table_name, columns = f'{folder}/years.json', f'{folder}_years', ['year', 'year_string']
  json_to_table(f'{years_json}', database_path, table_name, columns)

  series_json, table_name, columns = f'{folder}/series.json', f'{folder}_series', ['series', 'description']
  json_to_table(f'{series_json}', database_path, table_name, columns)

  countries_json, table_name, columns = f'{folder}/countries.json', f'{folder}_countries', ['country_code', 'country']
  json_to_table(f'{countries_json}', database_path, table_name, columns)


def load_all_data_from_db(folder: str, database_name: str):
  database_path = folder + '/' + database_name
  
  # csv from sql table
  table_name = f'{folder}_data'
  data = load_csv_from_database(database_path, table_name)

  table_name = f'{folder}_years'
  years = load_json_from_database(database_path, table_name)
  
  table_name = f'{folder}_series'
  series = load_json_from_database(database_path, table_name)

  table_name = f'{folder}_countries'
  countries = load_json_from_database(database_path, table_name)

  return data, years, series, countries

  

if __name__ == "__main__":
  save_all_data_to_db('preprocessed', 'world_data.db')
  load_all_data_from_db('preprocessed', 'world_data.db')