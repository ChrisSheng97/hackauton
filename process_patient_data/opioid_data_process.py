import csv

def process_opioid_table(table_loc):
    patient_id = 0
    data = {}
    with open(table_loc, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            this_patient_data = {}
            this_patient_data['death_date'] = row[0]
            this_patient_data['death_time'] = row[1]
            if row[2] == 'Accident':
                manner = 0
            else: # Accidents
                manner = 1
            this_patient_data['manner'] = manner
            this_patient_data['age'] = row[3]
            this_patient_data['sex'] = row[4]
            this_patient_data['gender'] = row[5]
            this_patient_data['case_dispo'] = row[6]
            # 7 ~ 13 (inclusive) 7 kinds of doses
            this_patient_data['doses'] = []
            for i in range(7, 14):
                if row[i] != '':
                    this_patient_data['doses'].append(row[i])
            print(this_patient_data['doses'])
            # incident_zip 14
            this_patient_data['incident_zip'] = row[14]
            # decedent_zip 15
            this_patient_data['decedent_zip'] = row[15]
            # case year 16
            this_patient_data['case_year'] = row[16]

if __name__ == "__main__":
    process_opioid_table('fatal_accidental_od_2015.csv')

