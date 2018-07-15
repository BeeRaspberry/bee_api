import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, \
    SQLAlchemyConnectionField
from bee_api.models import db_session, Country as CountryModel,\
    StateProvince as StateProvinceModel, Location as LocationModel, \
    Hive as HiveModel, HiveData as HiveDataModel, User as UserModel


# Custom validator
def must_not_be_blank(data):
    if not data:
        raise ValidationError('Data not provided.')


class Country(SQLAlchemyObjectType):
    class Meta:
        model = CountryModel
        interfaces = (relay.Node, )


class StateProvince(SQLAlchemyObjectType):
    class Meta:
        model = StateProvinceModel
        interfaces = (relay.Node, )


class Location(SQLAlchemyObjectType):
    class Meta:
        model = LocationModel
        interfaces = (relay.Node, )


class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        interfaces = (relay.Node, )


class Hive(SQLAlchemyObjectType):
    class Meta:
        model = HiveModel
        interfaces = (relay.Node, )


class HiveData(SQLAlchemyObjectType):
    class Meta:
        model = HiveDataModel
        interfaces = (relay.Node, )


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    all_states_provinces = SQLAlchemyConnectionField(StateProvince)
    all_locations = SQLAlchemyConnectionField(Location)
    all_users = SQLAlchemyConnectionField(User)
    all_hives = SQLAlchemyConnectionField(Hive)


schema = graphene.Schema(query=Query)
