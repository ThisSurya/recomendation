
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


def ClassProduct(data, key):

    data = data.loc[data['KODEPRODUK'] == key]
    kelas_product = data['KELASPRODUK'].reset_index(drop=True)

    return kelas_product[0]

def Recomendation_Best(data, key):
    data = data.loc[data['KELASPRODUK'] == key]
    data = data['KODEPRODUK'].unique()
    return data

def PickProduct(frequent):
    product = frequent['itemsets'].unique()
    product = list(product)

    if len(product) >= 10:
        product = product
    product = pd.DataFrame(product)
    return product

def Recomendation(association_result, key):
    key = [key]
    key = frozenset(key)

    association_result = association_result.loc[association_result['antecedents'] == key]
    list_recomendation = association_result['consequents']


    list_recomendation = list(list_recomendation)
    return list_recomendation