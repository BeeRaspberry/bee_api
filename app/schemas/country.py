import graphene
from graphene import (ID, Mutation, Connection, InputObjectType, String,
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
    short_name = String(description="Country Abbreviation.")


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
    class Arguments:
        name = String(description="Name of the Country.", required=True)
        short_name = String(description="Country Abbreviation.", required=True)

    ok = Boolean()
    Country = Field(CountryNode)
    message = String()

    def mutate(self, info, name, short_name):
        ok = True
        message = "Successfully Added"

        country = CountryModel(name=name, shortName=short_name)
        try:
            DB.session.add(country)
            DB.session.commit()
        except Exception as e:
            message = e
            ok = False
        
        return CreateCountry(Country=country, ok=ok, message=message)


class UpdateCountryInput(InputObjectType, CountryAttribute):
    id = graphene.ID(required=True, description="Global Id of the Country.")


class UpdateCountry(Mutation):
    class Arguments:
        id = ID(description="Country Id.", required=True)
        name = String(description="Name of the Country.")
        short_name = String(description="Country Abbreviation.")

    ok = Boolean()
    Country = Field(CountryNode)
    message = String()

    def mutate(self, info, id, name=None, short_name=None):
        ok = True
        message = "Successfully Updated"
        result = None

        try:
            query = CountryNode.get_query(info)
            result = query.filter(CountryModel.id==id)
            if short_name:
                result.shortName = short_name
            if name:
                result.name = name
            DB.session.commit()
        except Exception as e:
            message = e
            ok = False
        return UpdateCountry(ok=ok, Country=result, message=message)


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
