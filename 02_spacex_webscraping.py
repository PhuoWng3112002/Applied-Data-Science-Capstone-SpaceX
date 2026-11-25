import requests
from bs4 import BeautifulSoup
import unicodedata
import pandas as pd

def date_time(table_cells):
    return [data_time.strip() for data_time in list(table_cells.strings)][0:2]

def booster_version(table_cells):
    out = ''.join([booster_version for i, booster_version in enumerate(table_cells.strings) if i % 2 == 0][0:-1])
    return out

def landing_status(table_cells):
    return [i for i in table_cells.strings][0]

def get_mass(table_cells):
    mass = unicodedata.normalize("NFKD", table_cells.text).strip()
    if mass:
        new_mass = mass[0:mass.find("kg") + 2]
    else:
        new_mass = 0
    return new_mass

static_url = "https://en.wikipedia.org/w/index.php?title=List_of_Falcon_9_and_Falcon_Heavy_launches&oldid=1027686922"
response = requests.get(static_url)
soup = BeautifulSoup(response.text, 'html.parser')
html_tables = soup.find_all('table')

first_launch_table = html_tables[2]
column_names = []
for th in first_launch_table.find_all('th'):
    name = ' '.join(th.stripped_strings)
    if name is not None and len(name) > 0:
        column_names.append(name)

launch_dict = dict.fromkeys(column_names)
del launch_dict['Date and time ( )']
for key in ['Flight No.', 'Launch site', 'Payload', 'Payload mass', 'Orbit', 'Customer', 'Launch outcome', 'Version Booster', 'Booster landing', 'Date', 'Time']:
    launch_dict[key] = []

for table in soup.find_all('table', "wikitable plainrowheaders collapsible"):
    for rows in table.find_all("tr"):
        if rows.th and rows.th.string:
            flight_number = rows.th.string.strip()
            flag = flight_number.isdigit()
        else:
            flag = False
        row = rows.find_all('td')
        if flag:
            launch_dict['Flight No.'].append(flight_number)
            datatimelist = date_time(row[0])
            launch_dict['Date'].append(datatimelist[0].strip(','))
            launch_dict['Time'].append(datatimelist[1])
            bv = booster_version(row[1]) or row[1].a.string
            launch_dict['Version Booster'].append(bv)
            launch_dict['Launch site'].append(row[2].a.string)
            launch_dict['Payload'].append(row[3].a.string)
            launch_dict['Payload mass'].append(get_mass(row[4]))
            launch_dict['Orbit'].append(row[5].a.string)
            customer = row[6].a.string if row[6].a else row[6].text.strip()
            launch_dict['Customer'].append(customer)
            launch_dict['Launch outcome'].append(list(row[7].strings)[0])
            launch_dict['Booster landing'].append(landing_status(row[8]))

df_wiki = pd.DataFrame({key: pd.Series(value) for key, value in launch_dict.items()})
df_wiki.to_csv('spacex_web_scraped.csv', index=False)
print("Saved spacex_web_scraped.csv:", df_wiki.shape)