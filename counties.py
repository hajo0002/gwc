import pandas as pd

def get_county_df(state):
    base_url = 'https://en.wikipedia.org/wiki/List_of_counties_in_'
    url = base_url + state

    # get table from wikipedia
    df = pd.read_html(url, match='Etymology')[0]

    # rename columns to match db
    df.columns = ['county', 'fips_code', 'county_seat', 'est', 'origin', 'etymology', 'population', 'area', 'map']

    # remove irrelevant info
    df = df.drop(['county_seat', 'est', 'origin', 'etymology', 'map'], axis=1)

    # remove "County" from county name
    df['county'] = df['county'].str.replace(' County', '')

    # convert area from string to int
    df['area'] = pd.to_numeric(df['area'].str.split().str[0].str.replace(',', ''))
    
    return df

df = get_county_df('Illinois')
df.to_csv('il.csv', index=True)