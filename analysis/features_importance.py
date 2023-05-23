import json

import pandas as pd
from sklearn.linear_model import LinearRegression


df = pd.read_csv('../data/preprocessed/data.csv')
df.pop('country')

year = df.pop('year')
df_train = df[year == 2019]

with open('../data/preprocessed/series.json', 'r') as f:
    series = json.load(f)

gdp_pcap_log = df_train.pop('GDP.PCAP.LOG')

print(f'{"Significance":^15}|{"Series":^85}|{"Coefficient":^20}|{"Intercept":^20}')
print('-' * 140)

for i, col in enumerate(df_train.columns, start=1):
    lm = LinearRegression().fit(df_train[col].values.reshape(-1, 1), gdp_pcap_log)
    print(f'{i:>10}.    |{series[col]:85}|{lm.coef_[0]:^20.4f}|{lm.intercept_:^20.4f}')
