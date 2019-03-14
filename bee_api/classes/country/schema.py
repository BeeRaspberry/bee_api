import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType
from helpers import utils
from database import

from classes.country.model import Country as CountryModel


def check_country(data):
# Function expects 'data' to originate from StateProvince call.
    result = db.session.query(CountryModel). \
        filter_by(name=data['country']).first()
    if result is None:
        result = CountryModel(**data)
        db.session.add(result)
        db.session.commit()
    return result


class CountryAttribute:
    name = graphene.String(description="Name of the Country.")
    shortName = graphene.String(description="Country Abbreviation.")


class Country(SQLAlchemyObjectType, CountryAttribute):
    class Meta:
        model = CountryModel
        interfaces = (relay.Node,)


class CreateCountryInput(graphene.InputObjectType, CountryAttribute):
    pass


class CreateCountry(graphene.Mutation):
    country = graphene.Field(lambda: Country,
                             description="Country created by this mutation.")

    class Arguments:
        input = CreateCountryInput(required=True)

    def mutate(self, info, input):
        data = utils.input_to_dictionary(input)

        country = CountryModel(**data)
        db.session.add(country)
        db.session.commit()

        return CreateCountry(country=country)


class UpdateCountryInput(graphene.InputObjectType, CountryAttribute):
    id = graphene.ID(required=True, description="Global Id of the Country.")


class UpdateCountry(graphene.Mutation):
    Country = graphene.Field(lambda: Country, description="Country updated by this mutation.")

    class Arguments:
        input = UpdateCountryInput(required=True)

    def mutate(self, info, input):
        data = utils.input_to_dictionary(input)

        country = db.session.query(CountryModel).filter_by(id=data['id'])
        country.update(data)
        db.session.commit()
        country = db.session.query(CountryModel).filter_by(id=data['id']).first()

        return UpdateCountry(country=country)


class DeleteCountry(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        input = UpdateCountryInput(required=True)

    def mutate(self, info, input):
        data = utils.input_to_dictionary(input)

        country = db.session.query(CountryModel).filter_by(id=data['id'])
        country.delete()
        db.session.commit()

        return DeleteCountry(ok=True)
