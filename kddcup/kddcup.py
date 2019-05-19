import graphene
from flask import Flask
from flask_graphql import GraphQLView

app = Flask(__name__)


class Query(graphene.ObjectType):
    predict = graphene.String(packet=graphene.List(graphene.String))

    def resolve_predict(self, info, packet):
        return packet


schema = graphene.Schema(query=Query)


app.add_url_rule(
    '/kddcup-intrusion-detection-system', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))


if __name__ == "__main__":
    app.run(debug=True)
