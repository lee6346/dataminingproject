

#to create dicts for text representations of encoded attributes 
#ex: indicator dicts
def get_key_value_dict(df, code, name):
    return dict(zip(df.loc[:,code].unique(), df.loc[:,name].unique()))

#returns/generates attribute lists that can be merged
#will use to make pov_country_list and health_country_list
def attribute_list_generator(df, attr, transform=False):
    initial_list = df.loc[:,attr].unique()
    if not transform:
        return initial_list 
    def attribute_transform(standardized_list):
        for item in initial_list:
            if item in standardized_list:
                yield item 
    return attribute_transform

#merges attribute values using a dictionary (ex: country name discrepancies between two data sets)
def merge_attribute_values(df, attr, merge_dict):
    for key in merge_dict:
        df.loc[df[attr] == key, attr] = merge_dict[key]


#dropping attributes
def drop_attributes(df, attr_list, ax=1, ip=False):
    return df.drop(df.columns[attr_list], axis=ax, inplace=ip)

#set blank attributes to NaN
def set_to_null(df, attr, null_values):
    df.loc[df[attr].isin(null_values), attr] = np.nan

#get np array of a Series 
def get_column_values(df, col):
    return df[col].values

#should only use when all blank attributes have been converted to numpy.nan 
def is_usable(df, attr, axis=1, thresh=.3):
    return df.loc[:, attr].isnull().sum() / float(df.shape[0]) > thresh

#this function is specifically for the health/poverty attributes 
#it is chain of methods that drop columns, tranpose the shape, modifies data 
#so it can be merged with the terrorism data set 
def pre_merge_data_transformation(df, country, droplist):   
    return (df.loc[df['Country Name'] == country]
              .drop(dfpov.loc[:, droplist], axis=1)
              .set_index(['Indicator Code'])
              .rename_axis(None).T[2:]
              .assign(country_txt=lambda x: pd.Series([country for i in range(len(x))]).values)
              .reset_index(level=0)
              .rename(columns={'index':'iyear'})
              .assign(iyear=lambda x: pd.to_numeric(x['iyear'], errors='coerce'))
           )

#