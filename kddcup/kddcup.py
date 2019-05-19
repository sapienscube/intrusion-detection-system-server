import graphene
from flask import Flask
from flask_graphql import GraphQLView

app = Flask(__name__)


def fix_types(packet):
    example_packet = [0, 'icmp', 'ecr_i', 'SF', 1032, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 511,
                      511, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 255, 255, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 'smurf.']
    last_floats = [float(p) for p in packet[4:]]
    clean_packet = [float(packet[0]), packet[1],
                    packet[2], packet[3]] + last_floats
    return clean_packet


class Query(graphene.ObjectType):
    predict = graphene.String(packet=graphene.List(graphene.String))

    def resolve_predict(self, info, packet):
        clean_packet = fix_types(packet)
        print(clean_packet)
        return clean_packet


schema = graphene.Schema(query=Query)


app.add_url_rule(
    '/kddcup-intrusion-detection-system', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))


if __name__ == "__main__":
    app.run(debug=True)
