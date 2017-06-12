import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

page = requests.get('http://api.census.gov/data/2009/acs5/variables.html')
ACS_api_page = bs(page.text, 'lxml')

ACS_headers = ['Name', 'Label', 'Concept', 'Required', 'Limit', 'Predicate_Type']

ACS_rows = []

for tag in ACS_api_page.find_all(name='tr'):
    new_row = []
    for text in tag.find_all(name='td'):
        new_row.append(text.text)
        ACS_rows.append(new_row)

ACS = pd.DataFrame(ACS_rows, columns=ACS_headers)

ACS.to_csv('../datasets/housing-insights/ACS2009_api_vars.csv', header=False, encoding='utf-8')

ACS = pd.read_csv('../datasets/housing-insights/ACS2009_api_vars.csv', low_memory=False, encoding='utf-8')
ACS.set_index('0', inplace=True)
ACS.columns=ACS_headers
ACS.drop_duplicates(subset='Name', inplace=True)

from pandas.io import sql
import sqlite3
connection = sqlite3.connect('../datasets/housing-insights/ACS2009_api_vars.db.sqlite')
ACS.to_sql(name='ACS', con = connection, if_exists='replace', index=False)

def Q(query, db=connection):
    return sql.read_sql(query, db)
Q('SELECT * FROM ACS LIMIT 10')



poverty = Q('SELECT * FROM ACS WHERE Label LIKE "%below poverty%" AND Concept LIKE "%Age"')

labor = Q('SELECT * FROM ACS WHERE Label LIKE "%labor force%"')



''''
from original file

black_alone = Q('SELECT * FROM ACS WHERE Label LIKE "%Black or African American alone%"')
household_income = Q('SELECT * FROM ACS WHERE Label LIKE "%household income%"')
percap_income = Q('SELECT * FROM ACS WHERE Label LIKE "%per capita income%"')
foreign = Q('SELECT * FROM ACS WHERE Label LIKE "%foreign%"')
mother = Q('SELECT * FROM ACS WHERE Label LIKE "%Female Householder%"')
children = Q('SELECT * FROM ACS WHERE Label LIKE "%total%" AND Concept LIKE "%child%"')
divorced = Q('SELECT * FROM ACS WHERE Label LIKE "%divorce%"')
marriage = Q('SELECT * FROM ACS WHERE Label LIKE "%Total%" AND Concept LIKE "%marital%"')
total_pop = Q('SELECT * FROM ACS WHERE Label LIKE "%Total%" AND Concept LIKE "%population%"')

poverty_and_level = Q('SELECT * FROM ACS WHERE Label LIKE "%poverty level%"')

poverty_codes = Q('SELECT Name, Label FROM ACS WHERE Label LIKE "%poverty%"')

hispanic_all = Q('SELECT Name, Label FROM ACS WHERE Label LIKE "%ispanic%"')
'''