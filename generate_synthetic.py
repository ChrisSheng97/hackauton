import csv
import random
from datetime import date

overdose = []
synthetic = {}

AdmissionsCorePopulatedTable = open("./Data/10000-Patients/AdmissionsCorePopulatedTable.txt","r")
isHead = True
for line in AdmissionsCorePopulatedTable:
    if isHead:
        isHead = False
        continue
    fields = line.split("\t")
    PatientID = fields[0]
    AdmissionID = fields[1]
    AdmissionStartDate = fields[2]
    start_yr = int(AdmissionStartDate[:4])
    start_month = int(AdmissionStartDate[5:7])
    start_date = int(AdmissionStartDate[8:10])
    AdmissionEndDate = fields[3]
    end_yr = int(AdmissionEndDate[:4])
    end_month = int(AdmissionEndDate[5:7])
    end_date = int(AdmissionEndDate[8:10])
    d0 = date(start_yr, start_month, start_date)
    d1 = date(end_yr, end_month, end_date)
    DaysOfStay = (d1 - d0).days

    synthetic[PatientID] = {'DaysOfStay': DaysOfStay}

AdmissionsCorePopulatedTable.close()
# print(synthetic)


PatientCorePopulateTable = open("./Data/10000-Patients/PatientCorePopulatedTable.txt","r")
isHead = True
for line in PatientCorePopulateTable:
    if isHead:
        isHead = False
        continue
    fields = line.split("\t")
    PatientID = fields[0]
    Gender = fields[1]
    DateOfBirth = fields[2]
    Age = 2018 - int(DateOfBirth[:4])
    Race = fields[3]
    MaritalStatus = fields[4]
    Language = fields[5]
    PercentBelowPoverty = float(fields[6][:-1])/100

    data = {'Gender': Gender, 'Age': Age, 'Race': Race, 'MaritalStatus': MaritalStatus,
                    'Language': Language, 'PercentBelowPoverty': PercentBelowPoverty}
    for features in data:
        synthetic[PatientID][features] = data[features]

PatientCorePopulateTable.close()
# print(synthetic)


yrs = [i for i in range(2009, 2018)]
filename = ['fatal_accidental_od_%d.csv'%i for i in yrs]
num_patients = 0
total_age = 0
for f in filename:
    with open('./Data/allegheny/%s'%f) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            num_patients += 1
            overdoses = []
            for i in range(1, 8):
                col_name = 'Combined OD%d'%i
                if len(row[col_name]) > 0:
                    overdoses.append(row[col_name])
            # 'CaseYear': row['Case Year'],
            # 'DeathTime': row['Death Time']
            # 'Manner of Death': row['Manner of Death'],
            if row['Age'] == '':
                row['Age'] = -1
            else:
                total_age += int(row['Age'])
            overdose.append({'Age': int(row['Age']), 'Sex': row['Sex'], 'Race': row['Race'], 'Overdoses': overdoses})
avg_age = total_age/num_patients
for patient in overdose:
    if patient['Age'] == -1:
        patient['Age'] = avg_age

# print(overdose)

# overdose: 'Age': 55, 'Sex': 'Female', 'Race': 'White', 'Overdoses': ['Heroin', 'Fentanyl']

# synthetic: '7D6CA213-A8E8-4F92-9D1F-1BEDBE421CE0': {'DaysOfStay': 4, 'Gender': 'Male', 'Age': 64, 'Race': 'White', 'MaritalStatus': 'Widowed', 'Language': 'English', 'PercentBelowPoverty': 0.9293}


for patient in overdose:
    similar_patients = []
    for patientID in synthetic:
        # print(synthetic[patientID]['Gender'], synthetic[patientID]['Race'], synthetic[patientID]['Age'])
        if (synthetic[patientID]['Gender'] == patient['Sex'] and 
                    (synthetic[patientID]['Race'] == patient['Race'] or synthetic[patientID]['Race'] == 'Unknown') and 
                    abs(synthetic[patientID]['Age'] - patient['Age']) <= 100):
            similar_patients.append(patientID)
    match_ID = random.choice(similar_patients)
    # print(synthetic[match_ID])
    for features in synthetic[match_ID]:
        patient[features] = synthetic[match_ID][features]
    # del synthetic[ID]

# print(overdose)

output = []

top_drugs = ['Heroin', 'Fentanyl', 'Cocaine', 'Alcohol', 'Alprazolam', 'Oxycodone']
races = ['Unknown', 'Middle Eastern', 'Hispanic', 'Black', 'Asian', 'White']
languages = ['English', 'Icelandic', 'Unknown', 'Spanish']
MaritalStatus = ['Single', 'Married', 'Divorced', 'Separated', 'Unknown', 'Widowed']
with open('synthetic.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ')
    for row in overdose:
        drugs = [0,0,0,0,0,0,0]
        race = [0,0,0,0,0,0,0]
        language = [0,0,0,0]
        marital = [0,0,0,0,0,0,0]

        for drug in row['Overdoses']:
            if drug in top_drugs:
                idx = top_drugs.index(drug)
                drugs[idx] = 1
            else:
                drugs[6] = 1

        if row['Sex'] == 'Female':
            gender = 1
        else: gender = 0

        race_idx = races.index(row['Race'])
        race[race_idx] = 1

        language_idx = languages.index(row['Language'])
        language[language_idx] = 1

        marital_idx = MaritalStatus.index(row['MaritalStatus'])
        marital[marital_idx] = 1

        # languages[row['Language']] = True
        # MaritalStatus[row['MaritalStatus']] = True

        result = []
        for i in [row['Age'], gender, race, drugs, marital, language, 
                        row['PercentBelowPoverty']]:
            if (type(i) == list):
                result = result + i
            else:
                result.append(i)
        output.append(result)

        # print(row['Age'], gender, race, drugs, 
        #                 row['DaysOfStay'], marital, language, 
        #                 row['PercentBelowPoverty'])

        writer.writerow(result)

# add zipcode later
print(output)
