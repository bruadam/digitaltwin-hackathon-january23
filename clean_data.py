import pandas as pd
import openpyxl
import numpy as np
import datetime

## IMPORT CLIMIFY DATA

df = pd.read_csv(".\data\skylab_indoor_climate_dec_jan.csv")
# Clean time column by analyzing date from a string and convert to datetime
df['_time'] = pd.to_datetime(df['_time'].str[:10] + ' ' + df['_time'].str[11:19])

df   = df[(df['locationid'] == 229)|(df['locationid'] == 228)|(df['locationid'] == 227)|(df['locationid'] == 224)|(df['locationid'] == 212)]

# Clean Data
#df['locationid'] = df['locationid'].replace(df.loc[df['locationid'].str.contains('229')]['locationid'],'LEC-008-Skylab-3Dprint')
df['locationid'] = df['locationid'].replace(229, 'Print')
df['locationid'] = df['locationid'].replace(228, 'MultiLab')
df['locationid'] = df['locationid'].replace(227, 'DeveloperHall')
df['locationid'] = df['locationid'].replace(224, 'RapidPrototyping')
df['locationid'] = df['locationid'].replace(212, 'SkylabDigital')

# Group the dataframe by the attribute column
grouped = df.groupby('locationid')

# Iterate through each group and create a new dataframe for each group with the group name as the dataframe name
for name, group in grouped:
    globals()[name] = group 

# Combine the dataframes into one
data_climify = pd.concat([Print, MultiLab, DeveloperHall, RapidPrototyping, SkylabDigital])
# Create a new column that calculates the change in CO2 concentration over a 10-minute period
data_climify['co2_change'] = df['co2'].rolling(window=10).apply(lambda x: x[-1] - x[0], raw=True)

# Create a new column for occupancy
data_climify['occupancy_pred'] = 0

# Calculate occupancy for each room and add it to the dataframe given co2_change and motion values
for i, row in data_climify.iterrows():
    if row['co2_change'] > 10 and row['motion'] > 2: # If the co2_change is greater than 10 and motion is greater than 2, then the room is occupied
        data_climify.loc[i, 'occupancy_pred'] = 1  
    else:
        data_climify.loc[i, 'occupancy_pred'] = 0  

# # Export data_climify to Excel
data_climify.to_excel('.\cleandata\data_climify.xlsx')

## IMPORT OCCUPANCY FROM SKYLAB

df = pd.read_excel(".\data\DTU SkyLab Usage History Jan 2022_Jan 2023_NoNAME.xlsx")

# Clean the data and keep only the values for the Resource we are interested in
df = df[(df['Resource'] == 'LEC-008-Skylab-3Dprint')|(df['Resource'] == 'LEC-010-Skylab-Multi-Lab')|(df['Resource'] == 'LEC-008-Skylab-DeveloperHall')|(df['Resource'] == 'LEC-008-Skylab-RapidPrototyping')|(df['Resource'] == 'LEC-012-Skylab Digi')]
# Rename the Resource attributes to match the names in the climify data
df['Resource'] = df['Resource'].replace('LEC-008-Skylab-3Dprint', 'Print')
df['Resource'] = df['Resource'].replace('LEC-010-Skylab-Multi-Lab', 'MultiLab')
# df['Resource'] = df['Resource'].replace('LEC-008-Skylab-DeveloperHall', 'DeveloperHall')
# df['Resource'] = df['Resource'].replace('LEC-008-Skylab-RapidPrototyping', 'RapidPrototyping')
df['Resource'] = df['Resource'].replace('LEC-012-Skylab Digi', 'SkylabDigital')

# Convert the start and end dates to datetime
df['Usage Start'] = pd.to_datetime(df['Usage Start'])
df['Usage End'] = pd.to_datetime(df['Usage End'])

# Divide the data into groups based on the Resource attribute
grouped = df.groupby('Resource')

# Iterate through each group and create a new dataframe for each group with the group name as the dataframe name amd with dates as the index and occupancy as the column with 1s for the dates within the start and end date range
for name, group in grouped:
    globals()[name] = pd.DataFrame(index=pd.date_range(group['Usage Start'].min(), group['Usage End'].max()))
    for i, row in group.iterrows():
        globals()[name].loc[row['Usage Start']:row['Usage End'], 'occupancy'] = 1
# Add 0s for the dates outside the start and end date range for each dataframe
for name, group in grouped:
    globals()[name].fillna(0, inplace=True)
    
# Add a column in each dataframe with the corresponding name of the dataframe
for name, group in grouped:
    globals()[name]['locationid'] = name
# Combine the dataframes into one
data_skylab = pd.concat([Print, MultiLab, DeveloperHall, RapidPrototyping, SkylabDigital])

# Convert the date in index to a columm
data_skylab.reset_index(inplace=True)
data_skylab.rename(columns={'index': '_time'}, inplace=True)

# Export data_skylab to Excel
data_skylab.to_excel('.\cleandata\data_skylab.xlsx')