import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

"""
The following are generic functions that are used 
for grouping purposes
"""

#used to mine frequency patterns from non-numeric attributes
#ex: country frequency, frequency of weapon type and sub weapon type, etc 
def freq_grouping(df, attribute, attribute_val, dist_attr, dist_sub_attr=None):
    attr_list = [dist_attr]
    if dist_sub_attr is not None:
        attr_list.append(dist_sub_attr)
    return df[df[attribute] == attribute_val].groupby(attr_list)


#used to mine time-series patterns
def time_series_grouping(df, attributes, start=1974, end=2016):
    return df[(df.loc[:,'iyear'] >= start) & (df.loc[:,'iyear'] <= end)].loc[:,attributes + ['iyear', 'imonth']].groupby(['iyear', 'imonth'])



#using to retrieve totals in numerical data
def total_grouping(df, total_attr, start=1974):
    return (df.iloc[:,2:].set_index(['Indicator Name'])
                 .rename_axis(None)
                 .T[15:].dropna(axis=1, thresh=20)
                 .loc[:,total_attr].sum().values
            )



def get_numeric_attributes(df, ):
