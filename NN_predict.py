import pickle
import sys
sys.path.append('./model')
import NN as nn
sys.path.append('./process_patient_data')
import feature_extraction as fe
import match_data as md
import draw_general_samples as ds
from random import shuffle

pickle_file_name = './process_patient_data/' + fe.pickle_file_name

GEN_SAMPLE_NUM = 3000
def main():
    pkl_file = open(pickle_file_name, 'rb')
    _, patient_data, matched_data = pickle.load(pkl_file)
    pkl_file.close()
    # get training data
    # get OD data
    all_encodings, target_encoding = fe.extract_features(matched_data)
    bin_target_encoding = [[1] for i in range(len(target_encoding))]
    print('target_encoding num : {}'.format(len(target_encoding)))

    general_samples = ds.draw_general_sample(GEN_SAMPLE_NUM, patient_data, 'race', [0.805, 0.134, 0.037])
    print(len(matched_data))
    print(len(general_samples))
    general_sample_encodings, general_sample_target_encoding = fe.extract_features(general_samples, True)
    bin_general_sample_target_encoding = [[0] for i in range(len(general_sample_encodings))]
    print('general_encoding num : {}'.format(len(general_sample_target_encoding)))

    # create X and Y
    X = all_encodings
    X.extend(general_sample_encodings)
    # for categorical prediciton
    # Y = target_encoding
    # Y.extend(general_sample_target_encoding)
    # for binardy prediction Overdose vs non-Overdose
    Y = bin_target_encoding
    Y.extend(bin_general_sample_target_encoding)
    print(Y)
    # build NN model
    # for categorical prediction
    # nn_model = nn.NN(X, Y)
    # nn_model.train()
    # for binary prediction
    nn_model = nn.Bin_NN(X, Y)
    nn_model.train()


if __name__ == "__main__":
    main()