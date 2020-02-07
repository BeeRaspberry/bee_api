import graphene
from graphene import relay
from graphene_sqlalchemy import (SQLAlchemyObjectType,
                                 SQLAlchemyConnectionField)

from helpers import utils

from app import db
from .database import (Country as CountryModel, Location as LocationModel,
                       StateProvince as StateProvinceModel, Hive as HiveModel,
                       HiveData as HiveDataModel, User as UserModel)

__all__ = ['CreateCountry', 'UpdateCountry', 'CreateLocation',
           'UpdateLocation', 'CreateStateProvince', 'UpdateStateProvince']


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

    def mutate(self, info, input_value):
        data = utils.input_to_dictionary(input_value)

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

    def mutate(self, info, input_value):
        data = utils.input_to_dictionary(input_value)

        country = db.session.query(CountryModel).filter_by(id=data['id'])
        country.update(data)
        db.session.commit()
        country = db.session.query(CountryModel).filter_by(id=data['id']).first()

        return UpdateCountry(country=country)


class DeleteCountry(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        input = UpdateCountryInput(required=True)

    def mutate(self, info, input_value):
        data = utils.input_to_dictionary(input_value)

        country = db.session.query(CountryModel).filter_by(id=data['id'])
        country.delete()
        db.session.commit()

        return DeleteCountry(ok=True)


def check_location(data):
    result = db.session.query(LocationModel). \
        filter_by(street_address=data['street_address'],
                  city=data['city']).first()
    if result is None:
        result = LocationModel(**data)
        db.session.add(result)
        db.session.commit()
    return result


class LocationAttribute:
    street_address = graphene.String(description="Street Address")
    city = graphene.String(description="City Location")
    postal_code = graphene.String(description="Zip or Postal Code")
    state_province = graphene.String(description="Name of state, province, ")


class Location(SQLAlchemyObjectType):
    class Meta:
        model = LocationModel
        interfaces = (relay.Node, )


class CreateLocationInput(graphene.InputObjectType,
                          LocationAttribute):
    pass


class CreateLocation(graphene.Mutation):
    Location = graphene.Field(lambda: Location,
                description="StateProvince created by this mutation.")

    class Arguments:
        input = CreateLocationInput(required=True)

    def mutate(self, info, input_value):
        data = utils.input_to_dictionary(input_value)
        state_data = {'name': input['state_province']}
        state_province = check_state_province(state_data)
        data['state_province'] = state_province

        return CreateLocation(Location=check_location(data))


class UpdateLocationInput(graphene.InputObjectType,
                          LocationAttribute):
    id = graphene.ID(required=True,
                     description="Global Id of the Location.")


class UpdateLocation(graphene.Mutation):
    Location = graphene.Field(lambda: Location,
                    description="Location updated by this mutation.")

    class Arguments:
        input = UpdateLocationInput(required=True)

    def mutate(self, info, input_value):
        data = utils.input_to_dictionary(input_value)

        location = db.session.query(LocationModel).\
            filter_by(id=data['id'])
        location.update(data)
        db.session.commit()
        location = db.session.query(LocationModel).\
            filter_by(id=data['id']).first()

        return UpdateLocation(Location=location)


class DeleteLocation(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        input = UpdateLocationInput(required=True)

    def mutate(self, info, input_value):
        data = utils.input_to_dictionary(input_value)

        location = db.session.query(LocationModel).filter_by(id=data['id'])
        location.delete()
        db.session.commit()

        return DeleteLocation(ok=True)


def check_state_province(data):
    result = db.session.query(StateProvinceModel). \
        filter_by(name=data['name']).first()
    if result is None:
        result = StateProvinceModel(**data)
        db.session.add(result)
        db.session.commit()
    return result


class StateProvinceAttribute:
    name = graphene.String(description="Name of the State, Province, "
                                       "or Region.")
    country = graphene.String(description="Assign State, Province, or "
                                          "Region to this Country.")


class StateProvince(SQLAlchemyObjectType):
    class Meta:
        model = StateProvinceModel
        interfaces = (relay.Node, )


class CreateStateProvinceInput(graphene.InputObjectType,
                               StateProvinceAttribute):
    pass


class CreateStateProvince(graphene.Mutation):
    StateProvince = graphene.Field(lambda: StateProvince,
                description="StateProvince created by this mutation.")

    class Arguments:
        input = CreateStateProvinceInput(required=True)

    def mutate(self, info, input_value):
        data = utils.input_to_dictionary(input_value)

        return CreateStateProvince(StateProvince=check_state_province(data))


class UpdateStateProvinceInput(graphene.InputObjectType,
                               StateProvinceAttribute):
    id = graphene.ID(required=True,
                     description="Global Id of the StateProvince.")


class UpdateStateProvince(graphene.Mutation):
    StateProvince = graphene.Field(lambda: StateProvince,
                    description="StateProvince updated by this mutation.")

    class Arguments:
        input = UpdateStateProvinceInput(required=True)

    def mutate(self, info, input_value):
        data = utils.input_to_dictionary(input_value)

        state_province = db.session.query(StateProvinceModel).\
            filter_by(id=data['id'])
        state_province.update(data)
        db.session.commit()
        state_province = db.session.query(StateProvinceModel).\
            filter_by(id=data['id']).first()

        return UpdateStateProvince(StateProvince=state_province)


class DeleteStateProvince(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        input = UpdateStateProvinceInput(required=True)

    def mutate(self, info, input_value):
        data = utils.input_to_dictionary(input_value)

        province = db.session.query(StateProvinceModel).filter_by(id=data['id'])
        province.delete()
        db.session.commit()

        return DeleteStateProvince(ok=True)


class Hive(SQLAlchemyObjectType):
    class Meta:
        model = HiveModel
        interfaces = (relay.Node, )


class HiveData(SQLAlchemyObjectType):
    class Meta:
        model = HiveDataModel
        interfaces = (relay.Node, )


def check_user(data):
    return True


class AuthAttribute:
    email = graphene.String(description="Email")
    password = graphene.String(description="Password")


class Auth(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        interfaces = (relay.Node, )


class CheckAuthInput(graphene.InputObjectType, AuthAttribute):
    pass


class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        interfaces = (relay.Node, )


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    stateProvinceList = SQLAlchemyConnectionField(StateProvince)
    countryList = SQLAlchemyConnectionField(Country)
    locationList = SQLAlchemyConnectionField(Location)
    userList = SQLAlchemyConnectionField(User)
    hivesList = SQLAlchemyConnectionField(Hive)


class Mutation(graphene.ObjectType):
    createCountry = CreateCountry.Field()
    updateCountry = UpdateCountry.Field()
    deleteCountry = DeleteCountry.Field()
    createStateProvince = CreateStateProvince.Field()
    updateStateProvince = UpdateStateProvince.Field()
    deleteStateProvince = DeleteStateProvince.Field()
    createLocation = CreateLocation.Field()
    updateLocation = UpdateLocation.Field()
    deleteLocation = DeleteLocation.Field()
#    checkAuth = CheckAuth.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
