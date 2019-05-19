import graphene
from flask import Flask
from flask_graphql import GraphQLView
import pandas as pd

from detector import Detector

app = Flask(__name__)

encoders_dir = 'kddcup/encoders'
model_path = 'kddcup/models/kddcup-model-loss-0.0033-acc-99.94.h5'

d = Detector.from_path(encoders_dir, model_path)

header = ['0', 'tcp', 'http', 'SF', '184', '124', '0.1', '0.2', '0.3', '0.4', '0.5', '1', '0.6', '0.7', '0.8', '0.9', '0.10', '0.11', '0.12', '0.13', '0.14', '0.15', '1.1',
          '1.2', '0.00', '0.00.1', '0.00.2', '0.00.3', '1.00', '0.00.4', '0.00.5', '10', '10.1', '1.00.1', '0.00.6', '0.10.1', '0.00.7', '0.00.8', '0.00.9', '0.00.10', '0.00.11']

packet = [0, 'icmp', 'ecr_i', 'SF', 1032, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
          511, 511, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 255, 255, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0]

dfX = pd.DataFrame([packet], columns=header)
print(d.predict(dfX))


def fix_types(packet):
    example_packet = [0, 'icmp', 'ecr_i', 'SF', 1032, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 511,
                      511, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 255, 255, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 'smurf.']
    last_floats = [float(p) for p in packet[4:]]
    clean_packet = [float(packet[0]), packet[1],
                    packet[2], packet[3]] + last_floats
    return clean_packet


# df = pd.DataFrame([header, packet])
df = pd.read_csv('kddcup/manual_test.csv')
dfY = df[['normal.']]
dfX = df.drop(columns=['normal.'])


class Query(graphene.ObjectType):
    predict = graphene.String(packet=graphene.List(graphene.String))

    def resolve_predict(self, info, packet):
        # clean_packet = fix_types(packet)
        # print(clean_packet)
        return dfX.values.tolist()[0]


schema = graphene.Schema(query=Query)


app.add_url_rule(
    '/kddcup-intrusion-detection-system', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))


if __name__ == "__main__":
    app.run(debug=True)
