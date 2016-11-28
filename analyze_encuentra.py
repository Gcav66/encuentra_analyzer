# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 09:49:18 2016

@author: gus
"""

import pandas as pd
#   import matplotlib.pyplot as plt

def read_data(myFile):
    df = pd.read_excel(myFile)
    cdf = df.dropna()
    return cdf
    
def clean_data(myDF):
    new_df = myDF[['trimmed_name', 'clean_price', 'clean_mileage', 'clean_year', 'trim_name_year']]
    cdf = new_df[new_df.clean_price > 500]
    ndf = cdf[cdf.clean_year > 1989]
    mdf = ndf[ndf.clean_mileage < 400000]
    xdf = mdf[mdf.clean_price < 100000]
    gdf = xdf.drop(xdf[(xdf.clean_mileage < 100) & (xdf.clean_year <= 2014)].index)
    df = apply_bins(gdf)
    return df

def read_and_clean(myFile):
    df = read_data(myFile)
    new_df = clean_data(df)
    return new_df

def apply_bins(myDF):
    bins = range(0, 410000, 10000)
    myDF['miles_cat'] = pd.cut(myDF['clean_mileage'], bins, labels=bins[1:])
    return myDF

def get_prices(df, mycar, year):
    x = df[df.trimmed_name == mycar]
    #y = pd.pivot_table(x, values='clean_price', index=['miles_cat'], columns=['clean_year'])
    y = pd.pivot_table(x, values='clean_price', index=['clean_year', 'miles_cat'], aggfunc=('count', 
                       'mean', 'max', 'min'))
    z = y.ix[year]    
    #z = y.filter(like=str(year))
    #z.dropna(inplace=True)
    return z

def total(df, mycar, year):
    pivot = get_prices(df, mycar, year)
    final = pd.DataFrame(pivot)
    finito = format_money(final)
    return finito

def format_money(df):
    df['mean'] = df['mean'].map('${:,.2f}'.format)
    df['max'] = df['max'].map('${:,.2f}'.format)
    df['min'] = df['min'].map('${:,.2f}'.format)
    return df

"""
#df.plot(kind='scatter', x='clean_year', y='clean_price')
# create X and y
feature_cols = ['clean_year', 'clean_mileage']
X = df[feature_cols]
y = df.clean_price

# follow the usual sklearn pattern: import, instantiate, fit
from sklearn.linear_model import LinearRegression
lm = LinearRegression()
lm.fit(X, y)

# print intercept and coefficients
print lm.intercept_
print lm.coef_
"""
  
if __name__ == "__main__":
    """
    raw_df = read_data("encuentro_data_2.xlsx")
    df = clean_data(raw_df)
    pivot = get_prices('Toyota Corolla', 2015)
    raw_df = read_data("../encuentro_data_2.xlsx")
    df = clean_data(raw_df)
    #pivot = total("encuentro_data_2.xlsx", "Toyota Corolla", 2016)
    """
    
    