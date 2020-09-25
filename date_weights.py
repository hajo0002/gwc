import pandas as pd

# Load Walmart revenue data over time
df = pd.read_html('https://ycharts.com/companies/WMT/revenues')[0]
df.columns = ['date', 'revenue']

# Remove B from revenue
df.revenue = df.revenue.str.replace('B', '')

# Add last date to df
df = df.append({'date':'2020-09-30', 'revenue':134}, ignore_index=True)

# Convert column datatypes
df.revenue = pd.to_numeric(df.revenue)
df.date = pd.to_datetime(df.date)

# Set date as index
df = df.sort_values('date')
df = df.set_index('date')

# Fill in missing days (filled with Nones)
rev = df.revenue.asfreq('D')

# Interpolate data between points (4 per year)
rev_interp = rev.interpolate(method='polynomial', order=2)
df = pd.DataFrame(rev_interp)

# Our data starts in 2016
df = df[df.index >= '2016-01-01']

# Scale multipliers
scale = 1
normalized_df = (df - df.min()) / (df.max() - df.min()) * scale + (1 - scale / 2)

# Save
normalized_df.columns = ['multiplier']
normalized_df.to_csv('date_multipliers.csv')