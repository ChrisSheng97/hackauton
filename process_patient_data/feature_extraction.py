import match_data as md
import opioid_data_process as opi_process
import patient_data_process as pd_process

def extract_features():
    num_rank = 6
    opioid_data, patient_data, matched_data = md.match_data()
    print(matched_data)
    all_kinds, selected, percentage = opi_process.sort_important_doses(num_rank, [opioid_data])
    # matched_data
    # 2864: {'case_dispo': 'MO', 'gender': 'Female', 'age': '51', 
    #        'death_date': '12/31/2016', 'case_year': '2016', 'race': 'Black', 
    #        'manner': 0, 'doses': ['Citalopram/Escitalopram', 'Cocaine', 'Fentanyl'], 
    #        'death_time': '02:26 AM', 'decedent_zip': '15206', 'incident_zip': '15206'}
    
    # selected = ['Heroin', 'Cocaine', 'Alcohol', 'Fentanyl', 'Alprazolam', 'Oxycodone']



if __name__ == "__main__":
    extract_features()