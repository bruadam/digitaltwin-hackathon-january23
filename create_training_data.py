# import libraries
import pandas as pd
import numpy as np
import datetime

# Import data from excel files and create dataframes
df1 = pd.read_excel('.\cleandata\data_climify.xlsx')
df2 = pd.read_excel('.\cleandata\data_skylab.xlsx')

# Create a dataframe with the columns we need
df1 = df1[['_time', 'locationid', 'co2', 'humidity', 'temperature', 'light', 'motion']]

df2 = df2[['_time', 'ocupancy', 'locationid']]