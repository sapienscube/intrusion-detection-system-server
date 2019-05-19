import os
from detector import Detector

import pandas as pd

encoders_dir = 'kddcup/encoders'
model_path = 'kddcup/models/kddcup-model-loss-0.0033-acc-99.94.h5'

d = Detector.from_path(encoders_dir, model_path)
print(d)

header = ['0', 'tcp', 'http', 'SF', '184', '124', '0.1', '0.2', '0.3', '0.4', '0.5', '1', '0.6', '0.7', '0.8', '0.9', '0.10', '0.11', '0.12', '0.13', '0.14', '0.15', '1.1',
          '1.2', '0.00', '0.00.1', '0.00.2', '0.00.3', '1.00', '0.00.4', '0.00.5', '10', '10.1', '1.00.1', '0.00.6', '0.10.1', '0.00.7', '0.00.8', '0.00.9', '0.00.10', '0.00.11']

packet = [0, 'icmp', 'ecr_i', 'SF', 1032, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          511, 511, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 255, 255, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0]
print(len(packet))

dfX = pd.DataFrame([packet], columns=header)

# df = pd.read_csv('kddcup/manual_test.csv')
# dfY = df[['normal.']]
# dfX = df.drop(columns=['normal.'])
# print(df)

print(d.predict(dfX))
