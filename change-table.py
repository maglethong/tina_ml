import pandas as pd
import xlrd

file = 'C:\Data\GIT\__LOCAL_ONLY__\Tina\data\Diabetes_HR_für_Markus2.xlsm'

dataset = pd.read_excel(file, sheet_name='Probenübersicht')
dataset.sort_values(by=['Personen-index', 'History'])

#writing CSV
MAX_HISTORY = 150
SEPARATOR = ','
with open('C:\Data\GIT\__LOCAL_ONLY__\Tina\data\output.csv', 'w') as f:
    # writing header
    f.write('ID'+SEPARATOR+'OGTT'+SEPARATOR+'Lipo'+SEPARATOR+'')
    for i in range(MAX_HISTORY -1):
        f.write(str(i+1) + SEPARATOR)
    f.write(str(MAX_HISTORY) + '\n')

    curId = ''
    OGTT = ''
    curValues = ''

    for index, row in dataset.iterrows():
        # Stop if data finished
        if row['Personen-index'] == '':
            break

        # New ID
        if curId != row['Personen-index']:
            # Write data to CSV
            if curValues != '':
                # Every lip in its own row
                for lip in curValues:
                    f.write(str(curId) + SEPARATOR + str(OGTT) + SEPARATOR + str(lip))
                    # One column per history
                    for hist in range(1, MAX_HISTORY):
                        f.write(SEPARATOR + str(curValues[lip][hist]))
                    f.write('\n')


            # Reset data
            curId = row['Personen-index']
            OGTT = row['oGTT Ergebnis']
            curValues = {
                'Chylo. [A]': {},
                'Chylo. [B]': {},
                'Chylo. Rem': {},
                'VLDL [A]': {},
                'VLDL [B]': {},
                'IDL': {},
                'LDL [A]': {},
                'LDL [B]': {},
                'LDL [C]': {},
                'LDL [D]': {},
                'LDL [E]': {},
                'HDL [A]': {},
                'HDL [B]': {},
                'HDL [C]': {},
                'HDL [D]': {}
            }
            for lip in curValues:
                curValues[lip] = [''] * MAX_HISTORY

        # Save row in data
        try:
            h = int(row['History'])
            for lip in curValues:
                curValues[lip][h] = row[lip]
        except:
            print('Error at row ' + str(index))
            break
