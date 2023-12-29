import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# from apyori import apriori
from mlxtend.frequent_patterns import apriori, association_rules

def Rules(result_apriori):
    rules = association_rules(result_apriori, metric='lift', min_threshold=1)
    return rules

def Combination(rules_result, key_class):
    print(key_class)
    filtered = rules_result.loc[rules_result['antecedents'] == frozenset(key_class)]
    list_recomendation = filtered['consequents']
    print(list_recomendation)
    return list_recomendation