import graphene
from graphene import (Mutation, Connection, InputObjectType, String,
                      Field, Boolean, Node)
from graphene_sqlalchemy import (SQLAlchemyObjectType)
from app.database import (Hive as HiveModel,
                          HiveData as HiveDataModel)
from app import DB
from helpers.utils import input_to_dictionary
from .helpers import TotalCount
from app.filters import FilterConnectionField


class HiveNode(SQLAlchemyObjectType):
    class Meta:
        model = HiveModel
        interfaces = (Node,)
        connection_field_factory = FilterConnectionField.factory


class HiveConnection(Connection):
    """ Hive Connection """
    class Meta:
        """ Hive Connection """
        node = HiveNode
        interfaces = (TotalCount,)


class HiveDataNode(SQLAlchemyObjectType):
    class Meta:
        model = HiveDataModel
        interfaces = (Node,)
        connection_field_factory = FilterConnectionField.factory


class HiveDataConnection(Connection):
    """ HiveData Connection """
    class Meta:
        """ HiveData Connection """
        node = HiveDataNode
        interfaces = (TotalCount,)
