import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from apyori import apriori
from mlxtend.frequent_patterns import apriori, association_rules

import datetime

def Import_data():
    data_raw = pd.read_csv('Test_apriori.csv')
    data_raw['KODEPRODUK'] = data_raw['KODEPRODUK'].str.replace(" ", "")
    data_raw.drop_duplicates()
    data_raw = data_raw.dropna()

    return data_raw

def Choose_Customer(data_raw, key):
    key_customer = int(key)
    data_apriori = data_raw.loc[data_raw['CUSTOMERID'] == key]
    data_apriori = data_apriori.drop(['CUSTOMERID', 'KELASPRODUK'], axis=1)

    return data_apriori

def Time_Frame(data_apriori, timeframe):
    data_tf = [0 for x in range(0, timeframe)]
    for x in range(0, timeframe):
        data_tf[x] = data_apriori.loc[data_apriori['BLN'] == x+1].reset_index(drop=True)

    data_apriori = pd.concat(data_tf)
    data_apriori = data_apriori.reset_index(drop=True)
    return data_apriori

def Row2Column(data_apriori):
    data_apriori = data_apriori.pivot_table(index=['BLN', 'TGL'], columns='KODEPRODUK', fill_value=0, aggfunc=lambda x: 1)
    return data_apriori

def Modelling(data_apriori):
    frequent = apriori(data_apriori, min_support = 0.05, use_colnames=True)
    rules = association_rules(frequent, metric='lift', min_threshold=1)
    result = rules.sort_values(by = 'confidence', ascending = False)

    return frequent, result