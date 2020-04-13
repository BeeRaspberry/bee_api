import logging
from flask_graphql import GraphQLView
from .schema import schema
from app import app


@app.route('/')
def hello_world():
    logging.info('hello world')
    return 'Hello World!'


@app.route('/health')
def health_check():
    logging.info('Health Check')
    return 'ok'


app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True # for having the GraphiQL interface
    )
)
