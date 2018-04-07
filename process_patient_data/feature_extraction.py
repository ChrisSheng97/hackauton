import pickle
import match_data as md
import opioid_data_process as opi_process
import patient_data_process as pd_process
import numpy as np

IDC_10_NUM = 22
num_rank = 6

def extract_features():
    num_rank = 6
    # opioid_data, patient_data, matched_data = md.match_data()
    pkl_file = open('matched_data.pkl', 'rb')
    matched_data = pickle.load(pkl_file)
    pkl_file.close()
    # all_kinds, selected, percentage = opi_process.sort_important_doses(num_rank, [opioid_data])

    # matched_data
    # 2864: {'lang': 'English', 'diagnose': ['D30.21', 'M05.471', 'F68.11'], 
    #        'marital_status': 'Separated', 
    #        'case_dispo': 'MO', 'dob': '1968-09-22', 
    #        'gender': 'Female', 'age': '51', 
    #        'death_date': '12/31/2016', 
    #        'admission_dates': [('1987-03-04', '1987-03-16'), ('1990-11-11', '1990-11-25'), 
    #                            ('2012-08-04', '2012-08-11')], 
    #        'id': '82302D3A-D763-4930-8DDD-98B84124E7FD', 
    #        'case_year': '2016', 'race': 'Unknown', 
    #        'poverty': '14.38', 'manner': 0, 
    #        'doses': ['Citalopram/Escitalopram', 'Cocaine', 'Fentanyl'], 
    #        'death_time': '02:26 AM', 'decedent_zip': '15206', 'incident_zip': '15206'}

    # encoding features 
    matched_data_list = matched_data.values()
    general_features = ['lang', 'marital_status', 'gender', 'race']
    # general feature encoding
    feature_cats, feature_encodings = _general_encoding(matched_data_list, general_features)
    # DIAGNOSE 2 d list
    diagnose_encodings = _encode_diagnose(matched_data_list)
    # ENCODE ALL IN THIS ORDER:
    # age, poverty, diff_zip_code, case year(real number), manner (accident/accidents), 
    # lang, marital_status, gender, race (categorical), diagnose
    def is_int(s):
        try: 
            int(s)
            return True
        except ValueError:
            return False
    all_encodings = []
    for i in range(len(matched_data_list)):
        data = matched_data_list[i]
        diff_zip = abs(int(data['decedent_zip']) - int(data['incident_zip'])) \
            if is_int(data['decedent_zip']) and is_int(data['incident_zip']) \
            else 0
        p_encoding = [float(data['age']), float(data['poverty']), 
                      diff_zip, 
                      float(data['case_year']), int(data['manner'])]
        for feature in general_features:
            p_encoding.append(feature_encodings[feature][i])
        p_encoding.extend(diagnose_encodings[i])
        all_encodings.append(p_encoding)

    # encoding target/doses
    target_encoding = _encode_dose_target(matched_data_list, matched_data)
    return all_encodings, target_encoding

def _encode_dose_target(matched_data_list, matched_data):
    all_kinds, selected, percentage = opi_process.sort_important_doses(num_rank, [matched_data])
    # print(selected)
    all_encodings = []
    for data in matched_data_list:
        doses = data['doses']
        d_cats = [0 for i in range(len(selected) + 2)]
        for d in doses:
            if not d in selected:
                d_cats[len(selected)] += 1
            else:
                d_cats[selected.index(d)] += 1
        all_encodings.append(d_cats)
    return selected, all_encodings

def _general_encoding(matched_data_list, features_list):
    # generate features categories
    all_features_cats = {}
    for feature in features_list:
        all_features_cats[feature] = []
    for data in matched_data_list:
        for feature in features_list:
            certain_feature = data[feature]
            if not certain_feature in all_features_cats[feature]:
                all_features_cats[feature].append(certain_feature)
    # print(all_features_cats)
    # encode feature categories
    all_features_res = {}
    for feature in features_list:
        all_features_res[feature] = []
    for data in matched_data_list:
        for feature in features_list:
            certain_feature = data[feature]
            all_features_res[feature].append(all_features_cats[feature].index(certain_feature))
    return all_features_cats, all_features_res

def _encode_diagnose(matched_data_list):
    # encode directly according to ICD-10
    # res = np.zeros((0, IDC_10_NUM))
    res = []
    def encode_icd_10(icd_str):
        fst = icd_str.split('.')[0]
        fst_letter = fst[0]
        snd_letter_val = int(fst[1])
        if fst_letter == 'A' or fst_letter == 'B':
            return 0
        elif fst_letter == 'C' or (fst_letter == 'D' and snd_letter_val < 5):
            return 1
        elif fst_letter < 'S':
            return ord(fst_letter) - ord('A')
        elif fst_letter == 'S' or fst_letter == 'T':
            return 18
        elif fst_letter == 'V' or fst_letter == 'Y':
            return 19
        elif fst_letter == 'Z':
            return 20
        else:
            return 21
    for data in matched_data_list:
        # p_diag_all_cats = np.zeros(IDC_10_NUM)
        p_diag_all_cats = [0 for i in range(IDC_10_NUM)]
        diag = data['diagnose']
        for d in diag:
            d_code = encode_icd_10(d)
            p_diag_all_cats[d_code] += 1
        # res = np.vstack((res, p_diag_all_cats))
        res.append(p_diag_all_cats)
    return res

if __name__ == "__main__":
    all_encodings, target_encoding = extract_features()
