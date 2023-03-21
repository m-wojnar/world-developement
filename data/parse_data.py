import json
from argparse import ArgumentParser
from glob import glob

import numpy as np
import pandas as pd


DROP_ROWS = -5


def parse_data(df, output_dir):
    series = set(df['Series Code'])
    countries = set(df['Country Code'])
    years_dict = dict(map(lambda x: (int(x[:4]), x), df.columns[4:]))

    series_dict = {}
    country_dict = {}

    for s in series:
        series_dict[s] = df[df['Series Code'] == s].iloc[0]['Series Name']

    for c in countries:
        country_dict[c] = df[df['Country Code'] == c].iloc[0]['Country Name']

    data = pd.DataFrame(columns=['country', 'year'] + list(series_dict.keys()))

    for c in countries:
        for y in years_dict:
            tmp = df[df['Country Code'] == c]
            row = []

            for s in series:
                row.append(tmp[tmp['Series Code'] == s].iloc[0][years_dict[y]])

            data = data.append({
                'country': c,
                'year': y,
                **dict(zip(series_dict.keys(), row))
            }, ignore_index=True)

    data.replace('..', np.NAN, inplace=True)
    data.to_csv(f'{output_dir}/data.csv', index=False)

    with open(f'{output_dir}/countries.json', 'w') as fp:
        json.dump(country_dict, fp)
    
    with open(f'{output_dir}/series.json', 'w') as fp:
        json.dump(series_dict, fp)

    with open(f'{output_dir}/years.json', 'w') as fp:
        json.dump(years_dict, fp)

    return data, series_dict, country_dict, years_dict


if __name__ == '__main__':
    args = ArgumentParser()
    args.add_argument('--input_dir', default='.', type=str)
    args.add_argument('--output_dir', default='.', type=str)
    args = args.parse_args()

    df = None

    for file in glob(f'{args.input_dir}/*_Data.csv'):
        if df is None:
            df = pd.read_csv(file)
            df = df.iloc[:DROP_ROWS]
        else:
            new_df = pd.read_csv(file)
            new_df = new_df.iloc[:DROP_ROWS]
            df = pd.concat([df, new_df])

    parse_data(df, args.output_dir)
