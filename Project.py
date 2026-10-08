import re
import pandas as pd
import pdfplumber
from pathlib import Path
import glob

#Data from GSE annual statistcs report on solar panel from 2015 to 2024 
gse = pd.read_csv("dati/gse_province_panel (1).csv", sep=";", decimal=",")
print(gse.shape)
print(gse.head())

file_excel = sorted(Path("C:/Users/cecch/Desktop/rapporti fotovoltaico").glob("*.xlsx"))
print("File trovati:", len(file_excel))

# now we need to rename columns (from italian to english)
gse.rename(columns={
    'anno': 'Year',
    'regione': 'Region',
    'provincia': 'Province',
    'impianti': 'Number of plants',
    'mw': 'Power (MW)'
}, inplace=True)

# Data from TERNA on domestic consume from 2015 to 2024
# glob is just to read everything with the same root name 
path_file = glob.glob("dati/consume*.xlsx")

#create a list
list_data = []

# now we read every file and we add it to a list 
for file in path_file:
    # read the file
    df = pd.read_excel(file)
    # add to list
    list_data.append(df)

# concat all the table
consume = pd.concat(list_data, ignore_index=True)
print(consume.head())

# now we need to rename columns (from italian to english)
consume.rename(columns={
    'Anno': 'Year',
    'Regione': 'Region',
    'Provincia': 'Province',
    'Settore': 'Sector',
    'Consumo (GWh)': 'Consumption (GWh)'
}, inplace=True)
print(consume.head())
print(gse.head())