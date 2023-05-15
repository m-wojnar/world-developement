import pandas as pd
import sqlite3
import os


def csv_to_table(path: str, database: str, table: str):
  with sqlite3.connect(database) as conn:
    with open(path) as file:
      df = pd.read_csv(file)
    df.to_sql(table, conn)


def load_csv_from_database(database: str, table: str):
  with sqlite3.connect(database) as conn:
    query = f"SELECT * FROM {table}"
    df = pd.read_sql_query(query, conn)
    return df
  

if __name__ == "__main__":
  csv_name, database_name, table_name = 'selected/data.csv', 'test.db', 'Data'
  
  if os.path.exists(database_name):
    os.remove(database_name)

  csv_to_table('selected/data.csv', 'test.db', 'Data')
  print(load_csv_from_database('test.db', 'Data'))