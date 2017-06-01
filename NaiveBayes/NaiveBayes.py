import numpy as np
import pandas as pd
from collections import namedtuple



def CreateTable(col_n, series_in):
    TupleStructure = namedtuple(col_n,["uniqType","true_p","false_p"])
    u_type = series_in.unique()

    f_table = TupleStructure(
              uniqType=np.asarray(u_type),
              true_p=np.zeros(len(u_type)),
              false_p=np.zeros(len(u_type))
              )
    return f_table



def fillTable(i_type, series_in, series_t, truefalse=True):
    index_in = np.where(series_in == i_type)
    index_t = np.where(series_t == truefalse)
    molecular = len(np.intersect1d(index_in[0], index_t[0]))
    denominator = len(index_t[0])
    return molecular/denominator


def LaplacianSmoothing(i_type, series_in, series_t, truefalse=True, k=0):
    index_in = np.where(series_in == i_type)
    index_t = np.where(series_t == truefalse)
    molecular = len(np.intersect1d(index_in[0], index_t[0])) + k
    denominator = len(index_t[0]) + k*len(series_in.unique())
    return molecular/denominator


def CalculateNaiveBayes(table, features, queries):
    tp = 1
    fp = 1
    for f in features:
        idx = int(np.where(table[f].uniqType == queries[f])[0])
        tp = tp * list(table[f].true_p)[idx]
        fp = fp * list(table[f].false_p)[idx]
        
    return tp > fp

"""
CreateTable(col_n, series_in)

    col_n: column name(selected feature)
    series_in: pandas series

    f_table: naive bayes table for the selected feature



Example:
    small_table = CreateTable("Description", theft["Description"])

"""

"""
FillTable(i_type, series_in, series_t, truefalse=True)

    i_type: a category in a feature
    series_in: pandas series
    series_t: target pandas series(in our case it's "Arrest")
    truefalse: True or False.

    molecular/denominator: an array of conditional probability for each category in a feature


Example:
    col_n = "Description"
    tr_arr = list(map(lambda x: fillTable(x, theft[col_n], theft[target], True), theft[col_n].unique()))
    fa_arr = list(map(lambda x: fillTable(x, theft[col_n], theft[target], False), theft[col_n].unique()))
    small_table = small_table._replace(true_p=tr_arr)
    small_table = small_table._replace(false_p=fa_arr)





LaplacianSmoothing(i_type, series_in, series_t, truefalse=True, k=0)

    k: scale of smoothing. When k==0, the result will be the same as FillTable.


Example:
    col_n = "Description"
    LS0 = list(map(lambda x: fillTable(x, theft[col_n], theft[target], True, k=0), theft[col_n].unique()))
    LS1 = list(map(lambda x: fillTable(x, theft[col_n], theft[target], True, k=1), theft[col_n].unique()))
    dict_table[col_n] = dict_table[col_n]._replace(true_p=LS1)


"""

"""
CalculateNaiveBayes(table, features, queries)

    table: a list of small tabel
    features: an array of features
    queries: a row of dataframe


Example

    features = ['LocationDescription', 'Description', 'Domestic', 'Hour', 'Ward']
    answer = list(map(lambda x: CalculateNaiveBayes(big_table, features, theft_test.loc[x]), theft_test.index))

"""