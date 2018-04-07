import opioid_data_process as opi_process
import patient_data_process as pd_process
import random
from copy import deepcopy

list_opioid_table = ['fatal_accidental_od_2008.csv',
                     'fatal_accidental_od_2009.csv',
                     'fatal_accidental_od_2010.csv',
                     'fatal_accidental_od_2011.csv',
                     'fatal_accidental_od_2012.csv',
                     'fatal_accidental_od_2013.csv',
                     'fatal_accidental_od_2014.csv',
                     'fatal_accidental_od_2015.csv',
                     'fatal_accidental_od_2016.csv']

"""
  :param list_opioid_table : a list of opioid data tables
  :param patient_tables : self defined patient tables
"""
def match_data():
    # process opioid table first
    opioid_data_, num_opioid_patients = opi_process.process_opioid_table(list_opioid_table)
    # process patient_table
    patient_data = pd_process.process()
    def get_dob_year(dob_str):
        return dob_str.split('-')[0]
    opioid_data = deepcopy(opioid_data_)
    for p_id in opioid_data_:
        opioid_patient = opioid_data[p_id]
        similar_patients_ = {k : v for k , v in patient_data.iteritems() \
                             if (v['gender'] == opioid_patient['gender'] or v['gender'].lower() == 'unknown') \
                             and (opioid_patient['race'].lower() == v['race'].lower() or v['race'].lower() == 'unknown') \
                             and ( v['dob'] == '' or opioid_patient['case_year'] == '' \
                                   or opioid_patient['age'] == '' \
                                   or (abs(int(get_dob_year(v['dob'])) - (int(opioid_patient['case_year']) - int(opioid_patient['age']))) <= 5))}
        similar_patients = similar_patients_.keys()
        if len(similar_patients) == 0: # no similiar patients
            opioid_data.pop(p_id)
            continue
        match_id = random.choice(similar_patients)
        opioid_data[p_id]['id'] = match_id
        for feature in patient_data[match_id]:
            opioid_data[p_id][feature] = patient_data[match_id][feature]
        patient_data.pop(match_id)
    return opioid_data

if __name__ == "__main__":
    match_data()

