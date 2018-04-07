import csv
import random
from datetime import date

admissions = []
basics = []
overdose = []
synthetic = []

AdmissionsCorePopulatedTable = open("./Data/10000-Patients/AdmissionsCorePopulatedTable.txt","r")
for line in AdmissionsCorePopulatedTable:
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
    admissions.append({'PatientID': PatientID, 'AdmissionID': AdmissionID, 'DaysOfStay': DaysOfStay})
random.shuffle(admissions)
AdmissionsCorePopulatedTable.close()

PatientCorePopulateTable = open("./Data/10000-Patients/PatientCorePopulatedTable.txt","r")
for line in PatientCorePopulateTable:
    fields = line.split("\t")
    PatientID = fields[0]
    Gender = fields[1]
    DateOfBirth = fields[2]
    Age = 2018 - int(DateOfBirth[:4])
    Race = fields[3]
    MaritalStatus = fields[4]
    Language = fields[5]
    PercentBelowPoverty = fields[6]
    basics.append({'PatientID': PatientID, 'Gender': Gender, 'Age': Age, 'Race': Race, 'MaritalStatus': MaritalStatus,
                    'Language': Language, 'PercentBelowPoverty': PercentBelowPoverty})
random.shuffle(basics)
PatientCorePopulateTable.close()

yrs = [i for i in range(2009, 2018)]
filename = ['fatal_accidental_od_%d.csv'%i for i in yrs]
for f in filename:
    with open('./Data/allegheny/%s'%f) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            overdoses = []
            for i in range(1, 8):
                col_name = 'Combined OD%d'%i
                if len(row[col_name]) > 0:
                    overdoses.append(row[col_name])
            overdose.append({'DeathTime': row['Death Time'], 'Manner of Death': row['Manner of Death'],
                'Age': row['Age'], 'Sex': row['Sex'], 'Race': row['Race'], 'CaseYear': row['Case Year'],
                            'Overdoses': overdoses})

    random.shuffle(overdose)
    print(overdose)

# synthetic

# with open('synthetic.csv', 'wb') as csvfile:
#     writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
#     for i in range(0, train_total):
#         row = data[i]
#         writer.writerow([row['HR'], row['RR'], row['SPO2'], row['length'], row['pos_count'], row['neg_count']])



