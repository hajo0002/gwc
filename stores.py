import pandas as pd
import numpy as np

# Read csvs into pandas dataframe
counties = pd.read_csv('data/counties.csv')
retailers = pd.read_csv('data/retailers.csv')

# Create a store for each retailer in each county
store_id = 1
rows = []
for _, retailer in retailers.iterrows():
    for _, county in counties.iterrows():
        rows.append(
            {
                'store_id': store_id,
                'retailer_id': retailer.retailer_id,
                'county_id':  county.county_id
            }
        )
        store_id += 1
        
df = pd.DataFrame(rows)
df.to_csv('stores.csv', index=False)