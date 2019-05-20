import pandas as pd
import numpy as np
import pickle
import os
from sklearn.preprocessing import LabelEncoder, Normalizer, OneHotEncoder


class Preprocessor(object):
    protocol_type_encoder = LabelEncoder()
    service_encoder = LabelEncoder()
    flag_encoder = LabelEncoder()
    attack_type_encoder = OneHotEncoder()
    normalizer = Normalizer()

    # 'data' in the following methods is a pandas dataframe
    # representing the whole data read from the csv file

    def fitX(self, data):
        self.protocol_type_encoder.fit(data['protocol_type'])
        self.service_encoder.fit(data['service'])
        self.flag_encoder.fit(data['flag'])
        return self

    def fitY(self, data):
        dataY = data[['attack_type']]  # => don't modify 'data' directly
        dataY.loc[dataY['attack_type'] != 'normal.',
                  'attack_type'] = 'malicious'  # => 'data' not modified
        self.attack_type_encoder.fit(dataY)
        return self

    def transformX(self, dataX):
        # dataX should not contain the output label column
        self.protocol_type = self.protocol_type_encoder.transform(
            dataX['protocol_type'])
        self.service = self.service_encoder.transform(dataX['service'])
        self.flag = self.flag_encoder.transform(dataX['flag'])
        dataX['protocol_type'] = self.protocol_type
        dataX['service'] = self.service
        dataX['flag'] = self.flag
        dataX[dataX.columns] = self.normalizer.fit_transform(dataX)
        return dataX

    def transformY(self, dataY):
        # dataY is the output label column
        dataY.loc[dataY['attack_type'] != 'normal.',
                  'attack_type'] = 'malicious'  # => 'data' not modified
        lbY = self.attack_type_encoder.transform(dataY)
        return lbY.toarray()

    def inverse_transformY(self, dataY):
        return self.attack_type_encoder.inverse_transform(dataY)

    def save(self, path):
        with open(os.path.join(path, 'kddcup-protocol_type_encoder.pickle'), 'wb') as protocol_type_file:
            pickle.dump(self.protocol_type_encoder, protocol_type_file)
        with open(os.path.join(path, 'kddcup-service_encoder.pickle'), 'wb') as service_file:
            pickle.dump(self.service_encoder, service_file)
        with open(os.path.join(path, 'kddcup-flag_encoder.pickle'), 'wb') as sf_file:
            pickle.dump(self.flag_encoder, sf_file)
        with open(os.path.join(path, 'kddcup-attack_type_encoder.pickle'), 'wb') as lb_file:
            pickle.dump(self.attack_type_encoder, lb_file)

    @classmethod
    def load(cls, path):
        with open(os.path.join(path, 'kddcup-protocol_type_encoder.pickle'), 'rb') as protocol_type_file:
            cls.protocol_type_encoder = pickle.load(protocol_type_file)
        with open(os.path.join(path, 'kddcup-service_encoder.pickle'), 'rb') as service_file:
            cls.service_encoder = pickle.load(service_file)
        with open(os.path.join(path, 'kddcup-flag_encoder.pickle'), 'rb') as sf_file:
            cls.flag_encoder = pickle.load(sf_file)
        with open(os.path.join(path, 'kddcup-attack_type_encoder.pickle'), 'rb') as lb_file:
            cls.attack_type_encoder = pickle.load(lb_file)
        return cls()
