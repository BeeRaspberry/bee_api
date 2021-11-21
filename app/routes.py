import logging
from flask_graphql import GraphQLView
from .schema import SCHEMA
from app import APP


@APP.route('/')
def hello_world():
    logging.info('hello world')
    return 'Hello World!'


@APP.route('/health')
def health_check():
    logging.info('Health Check')
    return 'ok'


APP.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=SCHEMA,
        graphiql=True  # for having the GraphiQL interface
    )
)
