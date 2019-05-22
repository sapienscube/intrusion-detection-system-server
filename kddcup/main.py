import graphene
from flask import Flask
from flask_graphql import GraphQLView
from flask_cors import CORS
import pandas as pd

from detector import Detector

app = Flask(__name__)
CORS(app)


example_malicious_packet = ["0","icmp","ecr_i","SF","1032","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","511",
"511","0.0","0.0","0.0","0.0","1.0","0.0","0.0","255","255","1.0","0.0","1.0","0.0","0.0","0.0","0.0","0.0"]

example_normal_packet = ["0","tcp","http","SF","184","124","0","0","0","0","0","1","0","0","0","0","0","0","0","0","0","0","1","1","0.00","0.00","0.00","0.00","1.00","0.00","0.00","10","10","1.00","0.00","0.10","0.00","0.00","0.00","0.00","0.00"]

# Load preprocessors and model for prediction
preprocessor_path = 'kddcup/serialized-preprocessor'
model_path = 'kddcup/models/kddcup-model-loss-0.0039-acc-99.89.h5'
global d
d = Detector.from_path(preprocessor_path, model_path)

def fix_types(packets):
    clean_packets = []
    for packet in packets:
        last_floats = [float(p) for p in packet[4:]]
        clean_packet = [float(packet[0]), packet[1],
                        packet[2], packet[3]] + last_floats
        clean_packets.append(clean_packet)
    return clean_packets


class Query(graphene.ObjectType):
    predict = graphene.List(graphene.String, packets=graphene.List(graphene.List(graphene.String), description="A list of packets like these: " + "\n" + str([example_malicious_packet]) + "\n" + "\n" + "Where single quotes must be double quotes"))

    def resolve_predict(self, info, packets):
        # Cast number strings in packet to their types (float here)
        # clean_packets = fix_types(packets)

        # Format packet to a dataframe format
        names = ['duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes', 'land', 'wrong_fragment', 'urgent', 'hot', 'num_failed_logins', 'logged_in', 'num_compromised', 'root_shell', 'su_attempted', 'num_root', 'num_file_creations', 'num_shells', 'num_access_files', 'num_outbound_cmds', 'is_host_login', 'is_guest_login', 'count', 'srv_count', 'serror_rate',
         'srv_serror_rate', 'rerror_rate', 'srv_rerror_rate', 'same_srv_rate', 'diff_srv_rate', 'srv_diff_host_rate', 'dst_host_count', 'dst_host_srv_count', 'dst_host_same_srv_rate', 'dst_host_diff_srv_rate', 'dst_host_same_src_port_rate', 'dst_host_srv_diff_host_rate', 'dst_host_serror_rate', 'dst_host_srv_serror_rate', 'dst_host_rerror_rate', 'dst_host_srv_rerror_rate']
        dfX = pd.DataFrame(packets, columns=names)

        # Predict
        return d.predict(dfX)


schema = graphene.Schema(query=Query)


app.add_url_rule(
    '/intrusion-detection-system', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))


if __name__ == "__main__":
    app.run(debug=True)
