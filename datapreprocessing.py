

import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 



"""
The following are generic functions that are used 
for preprocessing but can be used during other processes
"""

# create dicts from two columns in a dataframe
# use case: when two columns are similar or represent each other in some way 
def get_key_value_dict(df, code, name):
    return dict(zip(df.loc[:,code].unique(), df.loc[:,name].unique()))


# generates list of specified items from dataframe
# use case: make list of country names from different data sets for future comparison
def attribute_list_generator(df, attr, transform=False):
    initial_list = df.loc[:,attr].unique()
    if not transform:
        return initial_list 
    def attribute_transform(standardized_list):
        for item in initial_list:
            if item in standardized_list:
                yield item 
    return attribute_transform


# merges attribute values using a dictionary 
# use case: country name discrepancies between two data sets
def merge_attribute_values(df, attr, merge_dict):
    for key in merge_dict:
        df.loc[df[attr] == key, attr] = merge_dict[key]


# replace values with new ones
# use case: imonth column uses 0 as a month, which we would like to be 1
def replace_column_values(df, attribute, current_val, new_val):
    df.loc[df[attribute] == current_val, attribute] = new_val
    return df 


# used to determine if a column/row has enough non null entries to be usable 
# use case: use to determine whether row/columns should be dropped/ignored
def is_usable(df, attr, axis=1, thresh=.3):
    return df.loc[:, attr].isnull().sum() / float(df.shape[0]) > thresh



"""
The following functions are specific for a type of data set or frame
and should limited in use 
"""

# used with health/poverty data structure. The chain transitions
# from dropping attributes using droplist, modifying indices, 
# transforming shapes, etc. until the df is ready to integrate. 
def pre_merge_data_transformation(df, country, droplist):   
    return (df.loc[df['Country Name'] == country]
              .drop(df.loc[:, droplist], axis=1)
              .set_index(['Indicator Code'])
              .rename_axis(None).T[2:]
              .assign(country_txt=lambda x: pd.Series([country for i in range(len(x))]).values)
              .reset_index(level=0)
              .rename(columns={'index':'iyear'})
              .assign(iyear=lambda x: pd.to_numeric(x['iyear'], errors='coerce'))
           )


# used with health/poverty data structure to drop unreliable attributes
# reliability fails if over half the column is null values
def drop_unreliable_attributes(df, attribute, value , min_thresh=.5, freq=.5):
    return ( df.loc[df[attribute] == value]
               .dropna(axis=1, thresh=(min_thresh * len(df)))
            )
    
# used with terrorism data to modify the date columns:
# 0 -> 1 for months/days, column name iyear -> year, 
# convert to date_format, then set as index for the data set 
# while removing them from ... 
def date_columns_to_index(df):
    return ( df.replace('.', np.NaN)
            .pipe(replace_column_values, 'imonth', 0, 1)
            .pipe(replace_column_values, 'iday', 0, 1)
            .rename(index=str, columns={'iyear': 'year', 'imonth': 'month', 'iday': 'day'})
            #.apply(lambda x: pd.to_datetime, x['year', 'month', 'day'])
            )
