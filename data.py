import pandas as pd
from typing import List


class Columns:
    sample_idx = 'Proben Index'         # numeric
    person_idx = 'Personen-index'       # eg: DS_231
    sample_number = 'History'           # numeric, lower is newest, if #1 present -> #1 (in theory) without eating
    sample_date = 'Spendedatum'         # dd.mm.yyyy
    oggt_date = 'Datum OGTT'            # dd/mm/yyyy OGTT (glucose tolerance test)
    ogtt_result = 'oGTT Ergebnis'       #
    ogtt_result_code = {    # TODO: Verify
        '1': 'healthy',
        '2': 'pre-diabetes',
        '3': 'pre-diabetes',
        '4': 'diabetes'
    }
    findrisk_score = 'Findrisk'         # numeric
    gender = 'Geschlecht'
    gender_code = {     # TODO: Verify
        '1': 'M',
        '2': 'F'
    }
    age = 'Alter'
    bmi = 'BMI'
    waist_size = 'Taillenumfang'
    height = 'Größe'
    weight = 'Gewicht'
    question_4 = 'Frage 4 Ernährung'    # boolean, Eats integral bread/veggies
    question_5 = 'Frage 5 Medis Blutthochdruck'  # boolean, Took meds against high pressure
    # Substances in: nano mol / L
    s01_chylo_a = 'Chylo. [A]'
    s02_chylo_b = 'Chylo. [B]'
    s03_chylo_rem = 'Chylo. Rem'
    s04_vldl_a = 'VLDL [A]'
    s05_vldl_b = 'VLDL [B]'
    s06_idl = 'IDL'
    s07_idl_a = 'LDL [A]'
    s08_idl_b = 'LDL [B]'
    s09_idl_c = 'LDL [C]'
    s10_idl_d = 'LDL [D]'
    s11_idl_e = 'LDL [E]'
    s12_hdl_a = 'HDL [A]'
    s13_hdl_b = 'HDL [B]'
    s14_hdl_c = 'HDL [C]'
    s15_hdl_d = 'HDL [D]'
    # Values from other sheet
    alt_person_idx = 'Label'        # Person index in alternative sheet
    gluc_0 = 'Glucose0_MgDl'        # Drink sugar test, value after 0s
    gluc_120 = 'Glucose120_MgDl'    # Drink sugar test, value after 120s
    hba1c = 'HBA1c'                 # Log time sugar test

    def read_excel(self, file):
        print("Reading File")
        dataset = pd.read_excel(file, sheet_name='Probenübersicht')

        data = List[Columns]

        for index, row in dataset.iterrows():

            if row[self.sample_idx] == "":
                break

            line = Columns()

            line.sample_idx = row[self.sample_idx]
            line.person_idx = row[self.person_idx]
            line.sample_number = row[self.sample_number]
            line.sample_date = row[self.sample_date]
            line.oggt_date = row[self.oggt_date]
            line.ogtt_result = row[self.ogtt_result]
            line.findrisk_score = row[self.findrisk_score]
            line.gender = row[self.gender]
            line.age = row[self.age]
            line.bmi = row[self.bmi]
            line.waist_size = row[self.waist_size]
            line.height = row[self.height]
            line.weight = row[self.weight]
            line.question_4 = row[self.question_4]
            line.question_5 = row[self.question_5]
            line.s01_chylo_a = row[self.s01_chylo_a]
            line.s02_chylo_b = row[self.s02_chylo_b]
            line.s03_chylo_rem = row[self.s03_chylo_rem]
            line.s04_vldl_a = row[self.s04_vldl_a]
            line.s05_vldl_b = row[self.s05_vldl_b]
            line.s06_idl = row[self.s06_idl]
            line.s07_idl_a = row[self.s07_idl_a]
            line.s08_idl_b = row[self.s08_idl_b]
            line.s09_idl_c = row[self.s09_idl_c]
            line.s10_idl_d = row[self.s10_idl_d]
            line.s11_idl_e = row[self.s11_idl_e]
            line.s12_hdl_a = row[self.s12_hdl_a]
            line.s13_hdl_b = row[self.s13_hdl_b]
            line.s14_hdl_c = row[self.s14_hdl_c]
            line.s15_hdl_d = row[self.s15_hdl_d]

            data.append(line)

        print("Reading additional info")
        dataset = pd.read_excel(file, sheet_name='neue oGTT-Daten')

        for index, row in dataset.iterrows():

            if row[self.alt_person_idx] == "":
                break

            alt_person_idx = row[self.alt_person_idx]

            for item in list(filter(lambda x: x.person_idx == alt_person_idx, data)):
                item.alt_person_idx = alt_person_idx
                item.gluc_0 = row[self.gluc_0]
                item.gluc_120 = row[self.gluc_120]
                item.hba1c = row[self.hba1c]

        return data




























