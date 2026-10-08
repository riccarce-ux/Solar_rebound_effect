import re
import pandas as pd
import pdfplumber
from pathlib import Path
import glob
import numpy as np
import matplotlib.pyplot as plt

#Data from GSE annual statistcs report on solar panel from 2015 to 2024 
gse = pd.read_csv("dati/gse_province_panel (1).csv", sep=";", decimal=",")
print(gse.shape)
print(gse.head())

file_excel = sorted(Path("C:/Users/cecch/Desktop/rapporti fotovoltaico").glob("*.xlsx"))
print("File trovati:", len(file_excel))

# now we need to rename columns (from italian to english)
gse.rename(columns={'anno': 'Year','regione': 'Region','provincia': 'Province','impianti': 'Number of plants','mw': 'Power (MW)'}, inplace=True)

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
consume.rename(columns={'Anno': 'Year','Regione': 'Region','Provincia': 'Province','Settore': 'Sector','Consumo (GWh)': 'Consumption (GWh)'}, inplace=True)
print(consume.head())
print(gse.head())



consumption_piemonte = consume[consume['Region'] == 'Piemonte']
solar_piemonte = gse[gse['Region'] == 'Piemonte']

# 2. Sum the data for each year (grouping all provinces in Piemonte)
annual_consumption = consumption_piemonte.groupby('Year')['Consumption (GWh)'].sum().reset_index()
annual_solar = solar_piemonte.groupby('Year')['Power (MW)'].sum().reset_index()

# 3. Merge the two grouped tables using the common 'Year' column
data_piemonte = pd.merge(annual_consumption, annual_solar, on='Year')

# 4. Prepare the variables (numpy expects 1D arrays)
X = data_piemonte['Power (MW)']
y = data_piemonte['Consumption (GWh)']

# 5. Perform linear regression using numpy (degree=1 for a straight line)
slope, intercept = np.polyfit(X, y, 1)

# --- REBOUND EFFECT CALCULATION ---

# 6. Define expected consumption decrease per installed MW
# Assuming 1.1 GWh/year of average production per 1 MW in Northern Italy
expected_slope = -1.1 

# 7. Apply the rebound effect formula
rebound_effect = ((expected_slope - slope) / expected_slope) * 100

print(f"Expected consumption variation: {expected_slope} GWh per MW")
print(f"Actual variation (calculated slope): {slope:.2f} GWh per MW")
print(f"ESTIMATED REBOUND EFFECT: {rebound_effect:.1f}%")

# 8. Terminal interpretation of the result
if rebound_effect < 0:
    print("No rebound effect: consumption dropped more than expected!")
elif 0 <= rebound_effect <= 100:
    print("Partial rebound effect: some clean energy was 'eaten' by new consumption.")
else:
    print("Backfire (Jevons Paradox): total consumption actually increased!")

# --- PLOTTING ---

# 9. Create a plot to visualize the result
plt.figure(figsize=(8, 5))
plt.scatter(X, y, color='blue', label='Real data (Piemonte)')

# Calculate the predicted values for the regression line using slope and intercept
y_predicted = (slope * X) + intercept
plt.plot(X, y_predicted, color='red', label='Regression line')

# Labels and title
plt.title('Relationship between Solar Power and Electricity Consumption in Piemonte')
plt.xlabel('Installed Solar Power (MW)')
plt.ylabel('Electricity Consumption (GWh)')
plt.legend()
plt.grid(True)

# Show the plot
plt.show()