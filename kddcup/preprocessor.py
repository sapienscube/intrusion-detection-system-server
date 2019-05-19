
import tensorflow as tf
import pandas as pd
import numpy as np
import pickle
import os
from sklearn.preprocessing import LabelEncoder, Normalizer, OneHotEncoder


class Preprocessor(object):
    tcp_encoder = LabelEncoder()
    http_encoder = LabelEncoder()
    sf_encoder = LabelEncoder()
    lb_encoder = OneHotEncoder()
    normalizer = Normalizer()

    # 'data' in the following methods is a pandas dataframe
    # representing the whole data read from the csv file

    def fitX(self, data):
        self.tcp_encoder.fit(data['tcp'])
        self.http_encoder.fit(data['http'])
        self.sf_encoder.fit(data['SF'])
        return self

    def fitY(self, data):
        dataY = data[['normal.']]  # => don't modify 'data' directly
        dataY.loc[dataY['normal.'] != 'normal.',
                  'normal.'] = 'malicious'  # => 'data' not modified
        self.lb_encoder.fit(dataY)
        return self

    def transformX(self, dataX):
        # dataX should not contain the output label column
        self.tcp = self.tcp_encoder.transform(dataX['tcp'])
        self.http = self.http_encoder.transform(dataX['http'])
        self.sf = self.sf_encoder.transform(dataX['SF'])
        dataX['tcp'] = self.tcp
        dataX['http'] = self.http
        dataX['SF'] = self.sf
        dataX[dataX.columns] = self.normalizer.fit_transform(dataX)
        return dataX

    def transformY(self, dataY):
        # dataY is the output label column
        dataY.loc[dataY['normal.'] != 'normal.',
                  'normal.'] = 'malicious'  # => 'data' not modified
        lbY = self.lb_encoder.transform(dataY)
        return lbY.toarray()

    def inverse_transformY(self, dataY):
        return self.lb_encoder.inverse_transform(dataY)

    def save(self, path):
        with open(os.path.join(path, 'kddcup-tcp_encoder.pickle'), 'wb') as tcp_file:
            pickle.dump(self.tcp_encoder, tcp_file)
        with open(os.path.join(path, 'kddcup-http_encoder.pickle'), 'wb') as http_file:
            pickle.dump(self.http_encoder, http_file)
        with open(os.path.join(path, 'kddcup-sf_encoder.pickle'), 'wb') as sf_file:
            pickle.dump(self.sf_encoder, sf_file)
        with open(os.path.join(path, 'kddcup-lb_encoder.pickle'), 'wb') as lb_file:
            pickle.dump(self.lb_encoder, lb_file)

    @classmethod
    def load(cls, path):
        with open(os.path.join(path, 'kddcup-tcp_encoder.pickle'), 'rb') as tcp_file:
            cls.tcp_encoder = pickle.load(tcp_file)
        with open(os.path.join(path, 'kddcup-http_encoder.pickle'), 'rb') as http_file:
            cls.http_encoder = pickle.load(http_file)
        with open(os.path.join(path, 'kddcup-sf_encoder.pickle'), 'rb') as sf_file:
            cls.sf_encoder = pickle.load(sf_file)
        with open(os.path.join(path, 'kddcup-lb_encoder.pickle'), 'rb') as lb_file:
            cls.lb_encoder = pickle.load(lb_file)
        return cls()
