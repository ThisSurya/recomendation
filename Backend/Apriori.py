import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from datetime import datetime
import joblib
# from apyori import apriori
from mlxtend.frequent_patterns import apriori, association_rules, fpgrowth

import datetime

def Import_data(data_raw):
    data_raw['KODEPRODUK'] = data_raw['KODEPRODUK'].str.replace(" ", "")
    data_raw['TGL'] = pd.to_datetime(data_raw.TGL, format="mixed", dayfirst=True)
    # data_raw['TGL'] = data_raw['TGL'].dt.strftime('%d/%m/%Y')


    data_raw['KOTA'] = data_raw['KOTA'].str.replace(" ", "")
    
    data_raw.drop_duplicates()
    
    data_cooked = data_raw.dropna()
    product = data_cooked[['KODEPRODUK', 'PRODUK GROUP']]
    data_cooked = data_cooked.drop(['AREA', 'CUSTOMERID', 'SHIPID', 'NAMAPELANGGAN', 'ALAMATPELANGGAN', 'NAMAPRODUK', 'BANYAK', 'PESAN', 'HNA', 'TOTHNA', '10,25% HNA', 'NILAIDOK', 'NET BU HNA', 'KODE SALUR', 'LINE', 'DM', 'MR', 'AP 1/2', 'TAHUN', 'KELASPRODUK', 'KODEPRODUK'], axis=1)
    
    data_cooked['KOTA'] = data_cooked['KOTA'].str.replace("KAB.TEGAL", "TEGAL")
    data_cooked['KOTA'] = data_cooked['KOTA'].str.replace("KOTATEGAL", "TEGAL")
    data_cooked['KOTA'] = data_cooked['KOTA'].str.replace("KAB.PEKALONGAN", "PEKALONGAN")
    data_cooked['KOTA'] = data_cooked['KOTA'].str.replace("KAB.BATANG", "BATANG")
    data_cooked['KOTA'] = data_cooked['KOTA'].str.replace("KAB.BREBES", "BREBES")
    data_cooked['KOTA'] = data_cooked['KOTA'].str.replace("KAB.PEMALANG", "PEMALANG")

    

    # data_cooked['PRODUK GROUP'] = data_cooked['PRODUK GROUP'].replace('2420001', 'Pabrik AA')
    # data_cooked['PRODUK GROUP'] = data_cooked['PRODUK GROUP'].replace('2420002', 'Pabrik AB')
    # data_cooked['PRODUK GROUP'] = data_cooked['PRODUK GROUP'].replace('2500001', 'Pabrik BA')
    # data_cooked['PRODUK GROUP'] = data_cooked['PRODUK GROUP'].replace('2500003', 'Pabrik BB')
    # data_cooked['PRODUK GROUP'] = data_cooked['PRODUK GROUP'].replace('3630001', 'Pabrik CA')
    # data_cooked['PRODUK GROUP'] = data_cooked['PRODUK GROUP'].replace('8011108', 'Pabrik DA')
    # data_cooked['PRODUK GROUP'] = data_cooked['PRODUK GROUP'].replace('8011109', 'Pabrik DB')
    # data_cooked['PRODUK GROUP'] = data_cooked['PRODUK GROUP'].replace('8011128', 'Pabrik DC')
    # data_cooked['PRODUK GROUP'] = data_cooked['PRODUK GROUP'].replace('8011129', 'Pabrik DD')
    # data_cooked['PRODUK GROUP'] = data_cooked['PRODUK GROUP'].replace('8011130', 'Pabrik DE')
    # data_cooked['PRODUK GROUP'] = data_cooked['PRODUK GROUP'].replace('8011B08', 'Pabrik DF')
    # data_cooked['PRODUK GROUP'] = data_cooked['PRODUK GROUP'].replace('8011B09', 'Pabrik DG')
    # data_cooked['PRODUK GROUP'] = data_cooked['PRODUK GROUP'].replace('8011B28', 'Pabrik DH')
    # data_cooked['PRODUK GROUP'] = data_cooked['PRODUK GROUP'].replace('8011B29', 'Pabrik DI')
    # data_cooked['PRODUK GROUP'] = data_cooked['PRODUK GROUP'].replace('8011B30', 'Pabrik DJ')
    # data_cooked['PRODUK GROUP'] = data_cooked['PRODUK GROUP'].replace('8050001', 'Pabrik DK')
    

    return data_cooked

def Dropping_col(data_cooked):
    data_cooked = data_cooked.drop(['AREA', 'CUSTOMERID', 'SHIPID', 'NAMAPELANGGAN', 'ALAMATPELANGGAN', 'NAMAPRODUK', 'BANYAK', 'PESAN', 'HNA', 'TOTHNA', '10,25% HNA', 'NILAIDOK', 'NET BU HNA', 'KODE SALUR', 'LINE', 'DM', 'MR', 'AP 1/2', 'TAHUN', 'KELASPRODUK', 'KODEPRODUK'], axis=1)
    return data_cooked

def Choose_City(data_cooked, key):
    data_cooked = data_cooked.loc[data_cooked['KOTA'] == key]
    data_cooked = data_cooked.drop(['KOTA'], axis=1)
    data_cooked = data_cooked.reset_index(drop=True)

    return data_cooked

def Time_Frame(data_cooked, tgl_awal, tgl_akhir):
    tgl_awal = tgl_awal.strftime("%d/%m/%Y")
    tgl_akhir = tgl_akhir.strftime("%d/%m/%Y")

    data_cooked['TGL'] = data_cooked['TGL'].dt.strftime("%d/%m/%Y")
    
    data_cooked = data_cooked[(data_cooked['TGL'] > tgl_awal) & (data_cooked['TGL'] < tgl_akhir)]
    data_cooked = data_cooked.reset_index(drop=True)
    return data_cooked

def CountAll(data_raw):
    all_class = data_raw['PRODUK GROUP'].unique()
    all_class = list(all_class)

def Row2Column(data_apriori):
    data_apriori = data_apriori.pivot_table(index=['TGL'], columns='PRODUK GROUP', fill_value=0, aggfunc=lambda x: 1)
    return data_apriori

def Modelling(data_apriori, support):
    support = float(support)
    frequent = fpgrowth(data_apriori, min_support = support, use_colnames=True)
    # rules = rules.sort_values(by = 'confidence', ascending = False)
    rules = ''

    frequent = frequent.sort_values(by='support', ascending=False)
    frequent = frequent.reset_index(drop=True)
    
    if len(frequent) < 1:
        st.write("Tidak ada data yang bisa ditampilkan")
    else:
        rules = association_rules(frequent, metric='lift', min_threshold=1)
        rules = rules[(rules['support'] > support)]
        rules = rules.sort_values(by='confidence', ascending=False)

    return frequent, rules

def RemoveFronzenset_Assoc(assoc_result):
    assoc_result = (assoc_result.explode('antecedents').reset_index(drop=True).explode('consequents').reset_index(drop=True))
    assoc_result = assoc_result[['antecedents', 'consequents', 'support', 'confidence', 'lift', 'leverage']]

    assoc_result = assoc_result.drop_duplicates(subset=['antecedents', 'consequents'])
    assoc_result = assoc_result.reset_index(drop=True)

    return assoc_result

def RemoveFrozenset_Frequent(Frequent_result):
    Frequent_result = (Frequent_result.explode('itemsets').reset_index(drop=True))
    return Frequent_result

def Frozen2List(result_apriori):
    data = [list(x) for x in result_apriori['itemsets']]
    # data = [x for sublist in data for x in sublist]

    return data

def Flat1Dimesion(list):
    data = np.array(list)
    data = np.unique(list)

    return data