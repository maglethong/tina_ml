import pandas as pd
import numpy as np
import os
from typing import List

# Reference: https://towardsdatascience.com/random-forest-in-python-24d0893d51c0

###################
#### Read data ####
###################
if not os.path.exists('data\\data.csv'):
    import xlrd
    print("Reading XLSX File")
    dataset = pd.read_excel('data\\Diabetes_HR_für_Markus2.xlsm', sheet_name='Probenübersicht', encoding='iso-8859-15')  #german

    print("Writing XLSX File")
    with open('data\\data.csv', "w") as f:
        for col in dataset.columns:
            f.write(col + ';')
        f.write(' \n')

        for index, row in dataset.iterrows():

            if row['Proben Index'] == "":
                break

            for col in dataset.columns:
                f.write(str(row[col]) + ';')
            f.write(' \n')

print("Reading CSV File")
dataset = pd.read_csv('data\\data.csv', encoding='iso-8859-15', sep=';')

########################
#### Pre-processing ####
########################

# Drop all but last measurement
dataset = dataset[dataset['History'] == 1]

#Drop uninteresting columns
dataset = dataset.drop(columns=[
    'Proben Index',
    'Personen-index',
    'History',
    'Original (BRK) Materialbezeichnung',
    'Label',
    'BRK_Label',
    'Probenbezeichnung LipoFIT',
    'Messnummer',
    'Auftragsid',
    'Spendedatum',
    'Datum OGTT',
    'Tage zwischen oGTT und Spendedatum',
    'Anzahl Rückstellproben',
    'nüchtern (n) oder ohne nüchternprobe (o)',
    'oGTT zu t=120 min:  Probenbezeichnung LipoFIT',
    'Größe',
    'Gewicht',
    ' ',
    'Findrisk',
    'Frage 4 Ernährung',
    'Frage 5 Medis Blutthochdruck'
])

# Remove rows with empty values
dataset = dataset.dropna()
# Alt:
# for col in dataset.columns:
#     dataset = dataset[dataset[col].notnull()]

# Decoding values
dataset['oGTT Ergebnis'] = dataset['oGTT Ergebnis'].map({
    1: 'Healthy',
    2: 'Pre-diabetes',
    3: 'Pre-diabetes',
    4: 'Diabetes',
    5: 'Diabetes'
})

# one-hot Encode multivalued columns
# dataset = pd.get_dummies(dataset)

# Labels are the values we want to predict
labels = np.array(dataset['oGTT Ergebnis'])

# Drop label column
dataset = dataset.drop(columns='oGTT Ergebnis')

# Saving feature names for later use
feature_list = list(dataset.columns)

# Convert to numpy array
dataset = np.array(dataset)









