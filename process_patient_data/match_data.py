import opioid_data_process as opi_process
import patient_data_process as pd_process

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
def match_data(list_opioid_table, patient_tables):
    # process opioid table first
    opioid_data, num_opioid_patients = opi_process.process_opioid_table(list_opioid_table)
    print(opioid_data)
    # process patient_table
    patient_data = pd_process.process()
    races = {}
    for pd in opioid_data:
        the_race = opioid_data[pd]['race']
        if not the_race in races:
            races[the_race] = 1
        else:
            races[the_race] += 1
    print(races)



if __name__ == "__main__":
    
    match_data(list_opioid_table, [])

