import graphene
from graphene import (Mutation, Connection, InputObjectType, String,
                      Field, Boolean, Node)
from graphene_sqlalchemy import (SQLAlchemyObjectType)
from app.database import Country as CountryModel
from app import DB
from helpers.utils import input_to_dictionary
from .helpers import TotalCount
from app.filters import FilterConnectionField


def check_country(data):
    # Function expects 'data' to originate from StateProvince call.
    result = DB.session.query(CountryModel). \
        filter_by(name=data['country']).first()
    if result is None:
        result = CountryModel(**data)
        DB.session.add(result)
        DB.session.commit()
    return result


class CountryAttribute:
    name = String(description="Name of the Country.")
    shortName = String(description="Country Abbreviation.")


class CountryNode(SQLAlchemyObjectType):
    """ Country Node """
    class Meta:
        """ Country Node """
        model = CountryModel
        interfaces = (Node,)
        connection_field_factory = FilterConnectionField.factory


class CountryConnection(Connection):
    """ Country Connection """
    class Meta:
        """ Country Connection """
        node = CountryNode
        interfaces = (TotalCount,)


class CreateCountryInput(InputObjectType, CountryAttribute):
    pass


class CreateCountry(Mutation):
    country = Field(lambda: CountryNode,
                    description="Country created by this mutation.")

    class Arguments:
        input = CreateCountryInput(required=True)

    def mutate(self, info, input_value):
        data = input_to_dictionary(input_value)

        country = CountryModel(**data)
        DB.session.add(country)
        DB.session.commit()

        return CreateCountry(country=country)


class UpdateCountryInput(InputObjectType, CountryAttribute):
    id = graphene.ID(required=True, description="Global Id of the Country.")


class UpdateCountry(Mutation):
    Country = Field(lambda: CountryNode,
                    description="Country updated by this mutation.")

    class Arguments:
        input = UpdateCountryInput(required=True)

    def mutate(self, info, input_value):
        data = input_to_dictionary(input_value)

        country = DB.session.query(CountryModel).filter_by(id=data['id'])
        country.update(data)
        DB.session.commit()
        country = DB.session.query(CountryModel).filter_by(
            id=data['id']).first()

        return UpdateCountry(country=country)


class DeleteCountry(Mutation):
    ok = Boolean()

    class Arguments:
        input = UpdateCountryInput(required=True)

    def mutate(self, info, input_value):
        data = input_to_dictionary(input_value)

        country = DB.session.query(CountryModel).filter_by(id=data['id'])
        country.delete()
        DB.session.commit()

        return DeleteCountry(ok=True)
