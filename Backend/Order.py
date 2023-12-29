
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from apyori import apriori
from mlxtend.frequent_patterns import apriori, association_rules

import datetime

def BestSeller(frequent_apriori):
    order = frequent_apriori.sort_values(by = 'support', ascending = False)
    order = order.reset_index(drop=True)

    best_order = order['itemsets'][0]
    list_best = list(best_order)

    return list_best

def ListProduk(data_cook, key):
    data_cook = data_cook.loc[data_cook['KELASPRODUK'] == key]
    data_cook = data_cook['PRODUK GROUP'].unique()

    if len(data_cook) >= 5:
        data_cook = data_cook[:4]

    return data_cook

# kemungkinan ngga dipake
def ClassProduct(data, key):

    data = data.loc[data['KODEPRODUK'] == key]
    kelas_product = data['KELASPRODUK'].reset_index(drop=True)

    return kelas_product[0]

def Recomendation_Best(data, key):
    data = data.loc[data['KELASPRODUK'] == key]
    data = data['KODEPRODUK'].unique()
    return data

# kemungkinan ngga dipake
def PickProduct(frequent):
    product = frequent['itemsets'].unique()
    product = list(product)

    if len(product) >= 10:
        product = product[:15]
    product = pd.DataFrame(product)
    return product

def Recomendation(result, key = None):

    association_result = result.loc[result['antecedents'] == key]
    association_result = association_result.sort_values(by='confidence', ascending=False)
    association_result = association_result.reset_index(drop=True)
    
    if len(association_result) >= 5:
        association_result = association_result.head(4)
    # association_result = association_result[(association_result['support'] >= 0.1) | (association_result['confidence'] >= 0.1)]
    product = list(association_result['consequents'])
    return product
def Decision(assoc_result, antecedent_key, consequent_key):
    antecedent_key = [antecedent_key]
    consequent_key = [consequent_key]

    antecedent_key = frozenset(antecedent_key)
    consequent_key = frozenset(consequent_key)

    Decision_result = assoc_result[(assoc_result['antecedents'] == antecedent_key) & (assoc_result['consequents'] == consequent_key)]

    Decision_result = (Decision_result.explode('antecedents').reset_index(drop=True).explode('consequents').reset_index(drop=True))
    Decision_result = Decision_result[['antecedents', 'consequents', 'support', 'confidence']]
    Decision_result = Decision_result.drop_duplicates(subset=['antecedents', 'consequents'])

    Decision_result = Decision_result.reset_index(drop=True)
    return Decision_result