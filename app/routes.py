from flask_graphql import GraphQLView
from . import schema
from app import app


@app.route('/')
def hello_world():
    print('hello world')
    return 'Hello World!'


app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True # for having the GraphiQL interface
    )
)
