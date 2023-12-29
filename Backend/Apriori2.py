import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# from apyori import apriori
from mlxtend.frequent_patterns import apriori, association_rules

import datetime

def Import_data():
    data_raw = pd.read_csv('Testing_apriori.csv')
    data_raw['KODEPRODUK'] = data_raw['KODEPRODUK'].str.replace(" ", "")
    data_raw.drop_duplicates()
    return data_raw

def Preprocessing1(data_raw):
    data_raw = data_raw.drop(['AREA', 'CUSTOMERID', 'SHIPID', 'NAMAPELANGGAN', 'ALAMATPELANGGAN', 'NAMAPRODUK', 'BANYAK', 'PESAN', 'HNA', 'TOTHNA', '10,25% HNA', 'NILAIDOK', 'NET BU HNA', 'KODE SALUR', 'LINE', 'DM', 'MR', 'AP 1/2', 'TAHUN', 'PRODUK GROUP', 'KODEPRODUK'], axis=1)
    data_apriori_1 = data_raw.dropna()


    return data_apriori_1

def Preprocessing2(data_raw):
    data_apriori_2 = data_raw.dropna()
    data_apriori_2 = data_apriori_2.drop(['PESAN', 'PROFIT', 'CUSTOMERID', 'KODEPRODUK', 'PRODUK GROUP'], axis=1)

    return data_apriori_2

def Class_Product(data_apriori_1, key):
    data_apriori_1 = data_apriori_1.loc[data_apriori_1['KELASPRODUK'] == key]
    data_apriori_1 = data_apriori_1.drop(['KELASPRODUK'], axis=1)

    return data_apriori_1

def Row2Column(data_apriori, column_name):
    data_apriori = data_apriori.pivot_table(index=['TGL'], columns=column_name, fill_value=0, aggfunc=lambda x: 1)

    return data_apriori

def AprioriModel(data_apriori):
    frequent = apriori(data_apriori.astype('bool'), min_support = 0.1, use_colnames=True)
    
    return frequent

def Recomendation_Place(result_apriori):
    filtered_frequent = result_apriori[result_apriori['support'] > 0.7]
    filtered_frequent = filtered_frequent.sort_values(by='support', ascending=False)
    filtered_frequent = filtered_frequent.reset_index(drop=True)

    return filtered_frequent

def Frozen2List(result_apriori):
    data = [list(x) for x in result_apriori['itemsets']]
    data = [x for sublist in data for x in sublist]

    return data

def Flat1Dimesion(list):
    data = np.array(list)
    data = np.unique(list)

    return data

def City_Filter(data_apriori_2, key):
    data_apriori_2 = data_apriori_2.loc[data_apriori_2['KOTA'] == key]
    data_apriori_2 = data_apriori_2.drop(['KOTA'], axis = 1)

    return data_apriori_2
