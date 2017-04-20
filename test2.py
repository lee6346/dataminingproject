"""
Procedure:
1. import libraries
2. read in csv files 
3. fill all blanks/periods with np.nan
4. create all dictionaries to map codes to names
5. remove all unecessary columns 
6. transform pov and health data 
7. merge with terrorism data with country/year as keys

"""

import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 
import datapreprocessing as dpp



dfterr = pd.read_csv('globalterrorismdb_0616dist.csv').replace('.', np.NaN)
dfpov = pd.read_csv('PovStatsData.csv')
dfhealth = pd.read_csv('health_nutrition.csv')



#data attributes that aren't needed
terrdlist = ['eventid', 'approxdate', 'ingroup', 'ingroup2', 'ingroup3',
                'related', 'specificity', 'INT_ANY', 'weapdetail', 'summary',
                'motive', 'propcomment', 'ransomnote', 'addnotes', 'alternative_txt',
                'attacktype1_txt', 'attacktype2_txt', 'attacktype3_txt', 'targtype1_txt',
                'targsubtype1_txt', 'natlty1_txt', 'targtype2_txt', 'targsubtype2_txt',
                'natlty2_txt', 'targtype3_txt', 'targsubtype3_txt', 'natlty3_txt',
                'claimmode_txt', 'claimmode2_txt', 'claimmode3_txt', 'weaptype1_txt',
                'weapsubtype1_txt', 'weaptype2_txt', 'weapsubtype2_txt', 'weaptype3_txt',
                'weapsubtype3_txt', 'weaptype4_txt', 'weapsubtype4_txt', 'propextent_txt',
                'hostkidoutcome_txt', 'region', 'country']
povdlist = ['Country Code', 'Indicator Name', 'Unnamed: 46']
healthdlist = ['Country Code', 'Indicator Name', 'Unnamed: 60']

#dictionaries to merge same countries
inter_dataset = {
    'Korea, Dem. People\xe2\x80\x99s Rep.' : 'North Korea',
    "Korea, Dem. People’s Rep." : 'North Korea',
    'Korea, Rep.' : 'South Korea',
    'Kyrgyz Republic' : 'Kyrgyzstan',
    'Congo, Dem. Rep.' : 'Democratic Republic of the Congo',
    'Macao SAR, China' : 'Macau',
    'Yemen, Rep.' : 'Yemen',
    'Russian Federation' : 'Russia',
    "Cote d'Ivoire" : 'Ivory Coast',
    'Macedonia, FYR' : 'Macedonia',
    'Gambia, The' : 'Gambia',
    'Timor-Leste' : 'East Timor',
    'Brunei Darussalam' : 'Brunei',
    'Bosnia and Herzegovina' : 'Bosnia-Herzegovina',
    'Lao PDR' : 'Laos',
    'Hong Kong SAR, China' : 'Hong Kong',
    'Egypt, Arab Rep.' : 'Egypt',
    'Iran, Islamic Rep.' : 'Iran',
    'West Bank and Gaza' :  'West Bank and Gaza Strip',
    'Bahamas, The' : 'Bahamas',
    'Syrian Arab Republic' : 'Syria',
    'Congo, Rep.' : 'Republic of the Congo',
    'Venezuela, RB' : 'Venezuela',
    'World' : 'International'
}

intra_dataset = {
    'East Germany (GDR)' : 'Germany',
    'West Germany (FRG)': 'Germany',
    'South Yemen' : 'Yemen',
    'North Yemen' : 'Yemen',
    'Zaire' : 'Republic of the Congo', 
    'Rhodesia' : 'Zimbabwe',
    "People's Republic of the Congo": 'Republic of the Congo',
    'Taiwan' : 'China', 
    'Soviet Union' : 'Russia', 
    'South Vietnam' : 'Vietnam',
    'Vatican City' : 'Italy'
}

#dictionaries for code-numbers and text representations
alt = dpp.get_key_value_dict(dfterr, 'alternative', 'alternative_txt')
atk_type = dpp.get_key_value_dict(dfterr, 'attacktype1', 'attacktype1_txt') #int val
target = dpp.get_key_value_dict(dfterr, 'targtype1', 'targtype1_txt') #int val
subtarget = dpp.get_key_value_dict(dfterr, 'targsubtype1', 'targsubtype1_txt')
nationality = dpp.get_key_value_dict(dfterr, 'natlty1', 'natlty1_txt') #ntlty2 has 2 keys to store
claim_mode = dpp.get_key_value_dict(dfterr, 'claimmode', 'claimmode_txt')
weapon_type = dpp.get_key_value_dict(dfterr, 'weaptype1', 'weaptype1_txt') #has int val, others have float
weapon_subtype = get_key_value_dict(dfterr, 'weapsubtype1', 'weapsubtype1_txt')
prop_damage = dpp.get_key_value_dict(dfterr, 'propextent', 'propextent_txt')
hostage_outcome = dpp.get_key_value_dict(dfterr, 'hostkidoutcome', 'hostkidoutcome_txt')

pov_indicator_dict = dpp.get_key_value_dict(dfpov, 'Indicator Code', 'Indicator Name')
health_indicator_dict = dpp.get_key_value_dict(dfhealth, 'Indicator Code', 'Indicator Name')


#remove unecessary columns
dfterr.drop(terrdlist, axis=1)

#merge attribute values using country dictionaries
dpp.merge_attribute_values(dfterr, 'country_txt', intra_dataset)
dpp.merge_attribute_values(dfpov, 'Country Name', inter_dataset)
dpp.merge_attribute_values(dfhealth, 'Country Name', inter_dataset)

#get list of countries for each data set 
terrcountrylist = dfterr['country_txt'].unique()

pov_country_generator = dpp.attribute_list_generator(dfpov, 'Country Name', True)
pov_country_list = [country for country in pov_country_generator(terrcountrylist)]

health_country_generator = dpp.attribute_list_generator(dfhealth, 'Country Name', True)
health_country_list = [country for country in health_country_generator(terrcountrylist)]

# pipe the dataset transformations with respect to the country, rejoin for integration 
pov_country_sets = [dpp.pre_merge_data_transformation(dfpov, c, povdlist) for c in pov_country_list]
health_country_sets = [dpp.pre_merge_data_transformation(dfhealth, c, healthdlist) for c in health_country_list]
tf_pov_data = pd.concat(pov_country_sets)
tf_health_data = pd.concat(health_country_sets)

#integrate all three datasets
data_store = pd.merge(dfterr, tf_pov_data, how='left', on=['iyear', 'country_txt']).merge(tf_health_data, how='left', on=['iyear', 'country_txt'])
