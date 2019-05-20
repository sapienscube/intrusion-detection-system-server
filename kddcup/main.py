import os
from detector import Detector

import pandas as pd

preprocessor = 'kddcup/serialized-preprocessor'
model_path = 'kddcup/models/kddcup-model-loss-0.0033-acc-99.94.h5'

d = Detector.from_path(preprocessor, model_path)
print(d)

names = ['duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes', 'land', 'wrong_fragment', 'urgent', 'hot', 'num_failed_logins', 'logged_in', 'num_compromised', 'root_shell', 'su_attempted', 'num_root', 'num_file_creations', 'num_shells', 'num_access_files', 'num_outbound_cmds', 'is_host_login', 'is_guest_login', 'count', 'srv_count', 'serror_rate',
         'srv_serror_rate', 'rerror_rate', 'srv_rerror_rate', 'same_srv_rate', 'diff_srv_rate', 'srv_diff_host_rate', 'dst_host_count', 'dst_host_srv_count', 'dst_host_same_srv_rate', 'dst_host_diff_srv_rate', 'dst_host_same_src_port_rate', 'dst_host_srv_diff_host_rate', 'dst_host_serror_rate', 'dst_host_srv_serror_rate', 'dst_host_rerror_rate', 'dst_host_srv_rerror_rate']
# packet = [0, 'icmp', 'ecr_i', 'SF', 1032, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#           511, 511, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 255, 255, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0]
# print(len(packet))

# dfX = pd.DataFrame([packet], columns=names)

df = pd.read_csv('kddcup/manual_test.csv', names=names+['attack_type'])
dfY = df['attack_type']
dfX = df.drop(columns=['attack_type'])
# print(df)

print(d.predict(dfX))
