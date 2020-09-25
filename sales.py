import pandas as pd
import numpy as np
from datetime import date, timedelta, datetime
import math
import random
import time
from os import path

# Load all data
counties = pd.read_csv('data/counties.csv')
manufacturers = pd.read_csv('data/manufacturers.csv')
products = pd.read_csv('data/products.csv')
retailers = pd.read_csv('data/retailers.csv')
stores = pd.read_csv('data/stores.csv')
date_multipliers = pd.read_csv('data/date_multipliers.csv')
product_multipliers = pd.read_csv('data/product_multipliers.csv')

# Add columns for ratios of rows to total
manufacturers['ratio'] = manufacturers.revenue / manufacturers.revenue.sum()
retailers['ratio'] = retailers.revenue / retailers.revenue.sum()
counties['ratio'] = counties.population / counties.population.sum()

# Only use first 5 manufacturers (6+ don't have products)
manufacturers = manufacturers[manufacturers.manufacturer_id <= 5]

start_date = date(2016, 1, 1)
end_date = date(2020, 9, 30)
curr_date = start_date

sales_per_day = 1000

sales_list = []
start = time.time()
# Loop over each day
while curr_date <= end_date:
    # Print time elapsed on 1st of each month
    if curr_date.day in [1]:
        print(f'[{curr_date}] {time.time()-start:.2f} s')
    
    # Get date multiplier
    date_mult = float(date_multipliers[date_multipliers.date == curr_date.strftime('%Y-%m-%d')].multiplier)
    
    for man in manufacturers.itertuples(index=False):
        
        # If manufacturer hasn't been added as of curr_date, skip the rest
        manufacturer_add_date = datetime.strptime(man.add_date, '%Y-%m-%d %H:%M:%S').date()
        if manufacturer_add_date > curr_date:
            continue
        
        # Get products made by current manufacturer
        man_products = products[products['manufacturer_id'] == man.manufacturer_id]
        man_products = man_products.merge(product_multipliers)
        man_products['prob'] = man_products['mult'] / man_products['mult'].sum()
        
        # Generate sales for each pair of retailers and counties for this manufacturer
        for ret in retailers.itertuples(index=False):
            for cou in counties.itertuples(index=False):
                
                # Calculate number of sales to generate
                sales_percent = ret.ratio * cou.ratio * man.ratio * date_mult
                pre_div = 1
                num_sales = pre_div * math.floor(sales_per_day / pre_div * sales_percent * np.random.normal(1, 0.1))
                
                # Generate each sale
                for _ in range(num_sales):
                    # Pick random products, price, and quantity
                    product_id = int(man_products.sample(weights=man_products['prob'])['product_id'])
                    unit_price = round(np.random.normal(10, 2), 2)
                    qty = math.ceil(np.random.exponential(2))
                    
                    date_formatted = curr_date.strftime("%Y-%m-%d 00:00:00")
                    store_id = int(stores[(stores.retailer_id == ret.retailer_id) & (stores.county_id == cou.county_id)]['store_id'])
                    
                    sales_list.append(
                        {
                            'store_id': store_id,
                            'product_id': product_id,
                            'date': date_formatted,
                            'unit_price': unit_price,
                            'qty': qty 
                        }
                    )
                    
    curr_date += timedelta(days=1)

df = pd.DataFrame(sales_list)
df.to_csv('sales1000_prodweights.csv', index=False)