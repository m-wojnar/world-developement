import pandas as pd
import numpy as np
import json


def evaluate_data(filename):
    df = pd.read_csv(filename)
    
    with open('./countries.json') as f:
        countries = json.load(f)
    with open('./years.json') as f:
        years = json.load(f)
    with open('./series.json') as f:
        series = json.load(f)

    years_eval = dict()
    series_eval = dict()

    not_null = np.invert(df.isnull())
    not_null_columns = not_null.sum(axis=0)
    not_null_rows = not_null.sum(axis=1)

    for i in range(len(df)):
        year = df.iloc[i, 1]
        years_eval[year] = years_eval.get(year, 0) + not_null_rows[i]

    print("-------- YEARS --------\n")
    for key, value in years_eval.items():
        years_eval[key] = value / (len(countries) * len(series))
        print(f'{key}: {years_eval[key]}')

    for i, el in enumerate(not_null_columns):
        series_eval[df.columns[i]] = el / (len(countries) * len(years))

    sorted_series_eval = sorted(list(series_eval.items())[2:], key=lambda x: x[1], reverse=True)

    print("\n\n-------- SERIES --------\n")
    for i, el in enumerate(sorted_series_eval[:100]):
        print(f'{i+1}. {series[el[0]]}: {el[1]}')





if __name__ == "__main__":
    evaluate_data('./data.csv')