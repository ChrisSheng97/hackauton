import pickle
import feature_extraction as fe

"""source : https://www.census.gov/quickfacts/fact/table/alleghenycountypennsylvania/PST045216 """
# gender
FEMALE_PERCENT = 0.517
# age
BELOW_18 = 0.189
OVER_65 = 0.18
# race
WHITE = 0.805
ASIAN = 0.037


def draw_general_sample():
    # load data from pickle file
    pkl_file = open(fe.pickle_file_name, 'rb')
    opioid_data_, modified_patient_data, opioid_data = pickle.load(pkl_file)
    pkl_file.close()
    # draw samples

    # group patient data:
    # gender -> age (<18, 18~65, >65) -> race (white, asian, other)
    # gender
    # female_group = 
