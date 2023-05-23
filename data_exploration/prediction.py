import json

import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor


df = pd.read_csv('../data/preprocessed/data.csv')
year = df.pop('year')
df.pop('country')

df_train = df[year == 2019]
df_test = df[year == 2020]

with open('../data/preprocessed/series.json', 'r') as f:
    series = json.load(f)

gdp_pcap_log = df_train.pop('GDP.PCAP.LOG')
gdp_pcap_test = df_test.pop('GDP.PCAP.LOG')

rf = RandomForestRegressor(n_estimators=100, max_depth=5).fit(df_train, gdp_pcap_log)
lm = LinearRegression().fit(df_train, gdp_pcap_log)
svm = SVR().fit(df_train, gdp_pcap_log)
tree = DecisionTreeRegressor(max_depth=5).fit(df_train, gdp_pcap_log)

rf_mse = mean_squared_error(gdp_pcap_test, rf.predict(df_test))
lm_mse = mean_squared_error(gdp_pcap_test, lm.predict(df_test))
svm_mse = mean_squared_error(gdp_pcap_test, svm.predict(df_test))
tree_mse = mean_squared_error(gdp_pcap_test, tree.predict(df_test))

print(f'SVM MSE:\t\t\t{svm_mse}')
print(f'Random forest MSE:\t{rf_mse}')
print(f'Linear model MSE:\t{lm_mse}')
print(f'Decision tree MSE:\t{tree_mse}')
