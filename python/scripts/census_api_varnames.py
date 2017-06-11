import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

page = requests.get('http://api.census.gov/data/2010/sf1/variables.html')
census_api_page = bs(page.text, 'lxml')

census_headers = ['Name', 'Label', 'Concept', 'Required', 'Limit', 'Predicate_Type']

census_rows = []

for tag in census_api_page.find_all(name='tr'):
    new_row = []
    for text in tag.find_all(name='td'):
        new_row.append(text.text)
        census_rows.append(new_row)

census = pd.DataFrame(census_rows, columns=census_headers)

census.to_csv('../datasets/housing-insights/census_api_vars.csv', header=False, encoding='utf-8')

census = pd.read_csv('../datasets/housing-insights/census_api_vars.csv', low_memory=False, encoding='utf-8')
census.set_index('0', inplace=True)
census.columns=census_headers


from pandas.io import sql
import sqlite3
connection = sqlite3.connect('../datasets/housing-insights/census_api_vars.db.sqlite')
census.to_sql(name='census', con = connection, if_exists='replace', index=False)

def Q(query, db=connection):
    return sql.read_sql(query, db)
Q('SELECT * FROM census LIMIT 10')




Q('SELECT Name, Label FROM census WHERE Label LIKE "%capita%" LIMIT 20')






'''
poverty_codes = Q('SELECT Name, Label FROM census WHERE Label LIKE "%poverty%"')
poverty_and_level = Q('SELECT Name, Label FROM census WHERE Label LIKE "%poverty level%"')
hispanic_all = Q('SELECT Name, Label FROM census WHERE Label LIKE "%ispanic%"')
'''