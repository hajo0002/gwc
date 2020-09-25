import pandas as pd
import numpy as np

# Load and merge product and nutrition data
df = pd.read_csv('data/products.csv').merge(pd.read_csv('data/nutrition.csv'))

# Set index and drop unused columns
df = df.set_index('product_id')
df = df.drop(['manufacturer_id', 'name', 'department'], axis=1)

# Replace categories with relative arbitrary numbers/rankings
types = {'Plated':5, 'Bowl':4, 'Flatbread':2, 'Soup':3, 'Dessert':1}
df['type'] = df['type'].apply(lambda x: types[x])

categories = {'Poultry':4, 'Meat':8, 'Vegetarian':3, 'Seafood':1, 'Pasta':2}
df['category'] = df['category'].apply(lambda x: categories[x])

# Convert categories to numeric
df['type'] = pd.to_numeric(df['type'])
df['category'] = pd.to_numeric(df['category'])

# Scale data
dev = 0.2 # Max deviation (0.1 means multiplier will be between 0.9 and 1.1)
df = (df - df.min()) / (df.max() - df.min()) * 2 * dev + (1 - dev)

multipliers = df.product(axis=1)

pd.DataFrame(multipliers, columns=['mult']).to_csv('data/product_multipliers.csv')