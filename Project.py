import re
import pandas as pd
import pdfplumber

#Data from GSE annual statistcs report on solar panel from 2016 to 2024 
gse = pd.read_csv("dati/gse_province_panel (1).csv", sep=";", decimal=",")
print(gse.shape)
print(gse.head())