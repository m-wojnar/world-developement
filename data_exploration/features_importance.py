import json

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


df = pd.read_csv('../data/preprocessed/data.csv')
year = df.pop('year')
df_train = df[year == 2019]
df_test = df[year == 2020]

with open('../data/preprocessed/series.json', 'r') as f:
    series = json.load(f)

gdp_pcap = np.exp(df_train['GDP.PCAP.LOG'])

print(f'{"Significance":^15}|{"Series":^85}|{"Coefficient":^20}|{"Intercept":^20}')
print('-' * 140)

for i, col in enumerate(df.columns[:-2], start=1):
    if col in series:
        lm = LinearRegression().fit(df_train[col].values.reshape(-1, 1), gdp_pcap)
        print(f'{i:>10}.    |{series[col]:85}|{lm.coef_[0]:^20.4f}|{lm.intercept_:^20.4f}')
