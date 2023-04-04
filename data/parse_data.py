import json
from argparse import ArgumentParser
from glob import glob

import numpy as np
import pandas as pd


DROP_ROWS = -5


def parse_data(df, output_dir):
    years_dict = dict(map(lambda x: (int(x[:4]), x), df.columns[4:]))
    series_dict = {row[0]: row[1] for row in df[['Series Code', 'Series Name']].drop_duplicates().values}
    countries_dict = {row[0]: row[1] for row in df[['Country Code', 'Country Name']].drop_duplicates().values}

    columns = ['country', 'year'] + list(series_dict.keys())

    data = pd.DataFrame(np.empty((len(countries_dict) * len(years_dict), len(columns))), columns=columns)
    data['country'] = data['country'].astype(str)
    data['year'] = data['year'].astype(int)

    row_index = 0

    for ix, c in enumerate(countries_dict):
        print(ix, c)
        df_c = df[df['Country Code'] == c]

        for y in years_dict:
            df_y = df_c[['Series Code', years_dict[y]]]
            df_y = df_y.dropna()
            df_y = df_y.set_index('Series Code')
            df_y = df_y.replace('..', np.NAN)

            data.iloc[row_index] = [c, y] + df_y.loc[columns[2:]].values.squeeze().tolist()
            row_index += 1

    data = data.sort_values(by=['country', 'year'])
    data.to_csv(f'{output_dir}/data.csv', index=False)

    with open(f'{output_dir}/countries.json', 'w') as fp:
        json.dump(countries_dict, fp)
    
    with open(f'{output_dir}/series.json', 'w') as fp:
        json.dump(series_dict, fp)

    with open(f'{output_dir}/years.json', 'w') as fp:
        json.dump(years_dict, fp)

    return data, series_dict, countries_dict, years_dict


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
