import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, \
    SQLAlchemyConnectionField
from bee_api.helpers import utils
from bee_api.database import db_session
from bee_api.models import Location as LocationModel, Country as CountryModel,\
    Hive as HiveModel, StateProvince as StateProvinceModel, \
    Hive as HiveModel, HiveData as HiveDataModel, User as UserModel


# Custom validator
def must_not_be_blank(data):
    if not data:
        raise ValidationError('Data not provided.')


def check_country(data):
# Function expects 'data' to originate from StateProvince call.
    result = db_session.query(CountryModel). \
        filter_by(name=data['country']).first()
    if result is None:
        result = CountryModel(**data)
        db_session.add(result)
        db_session.commit()
    return result


def check_state_province(data):
    result = db_session.query(StateProvinceModel). \
        filter_by(name=data['name']).first()
    if result is None:
        result = StateProvinceModel(**data)
        db_session.add(result)
        db_session.commit()
    return result


def check_location(data):
    result = db_session.query(LocationModel). \
        filter_by(street_address=data['street_address'],
                  city=data['city']).first()
    if result is None:
        result = LocationModel(**data)
        db_session.add(result)
        db_session.commit()
    return result


class CountryAttribute:
    name = graphene.String(description="Name of the Country.")


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
        db_session.add(country)
        db_session.commit()

        return CreateCountry(country=country)


class UpdateCountryInput(graphene.InputObjectType, CountryAttribute):
    id = graphene.ID(required=True, description="Global Id of the Country.")


class UpdateCountry(graphene.Mutation):
    Country = graphene.Field(lambda: Country, description="Country updated by this mutation.")

    class Arguments:
        input = UpdateCountryInput(required=True)

    def mutate(self, info, input):
        data = utils.input_to_dictionary(input)

        country = db_session.query(CountryModel).filter_by(id=data['id'])
        country.update(data)
        db_session.commit()
        country = db_session.query(CountryModel).filter_by(id=data['id']).first()

        return UpdateCountry(country=country)


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

    def mutate(self, info, input):
        data = utils.input_to_dictionary(input)
        country_data = {'country': data['country']}
        country = check_country(country_data)
        StateProvince = check_state_province(data)

        return CreateStateProvince(StateProvince=StateProvince)


class UpdateStateProvinceInput(graphene.InputObjectType,
                               StateProvinceAttribute):
    id = graphene.ID(required=True,
                     description="Global Id of the StateProvince.")


class UpdateStateProvince(graphene.Mutation):
    StateProvince = graphene.Field(lambda: StateProvince,
                    description="StateProvince updated by this mutation.")

    class Arguments:
        input = UpdateStateProvinceInput(required=True)

    def mutate(self, info, input):
        data = utils.input_to_dictionary(input)

        StateProvince = db_session.query(StateProvinceModel).\
            filter_by(id=data['id'])
        StateProvince.update(data)
        db_session.commit()
        StateProvince = db_session.query(StateProvinceModel).\
            filter_by(id=data['id']).first()

        return UpdateStateProvince(StateProvince=StateProvince)


class LocationAttribute:
    street_address = graphene.String(description="Street Address")
    city = graphene.String(description="City Location")
    postal_code = graphene.String(description="Zip or Postal Code")
    street_address = graphene.String(description="Street Address")
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

    def mutate(self, info, input):
        data = utils.input_to_dictionary(input)
        state_data = {'name': input['state_province']}
        state_province = check_state_province(state_data)
        data['state_province'] = state_province
        Location = check_location(data)

        return CreateLocation(Location=Location)


class UpdateLocationInput(graphene.InputObjectType,
                          LocationAttribute):
    id = graphene.ID(required=True,
                     description="Global Id of the Location.")


class UpdateLocation(graphene.Mutation):
    Location = graphene.Field(lambda: Location,
                    description="Location updated by this mutation.")

    class Arguments:
        input = UpdateLocationInput(required=True)

    def mutate(self, info, input):
        data = utils.input_to_dictionary(input)

        Location = db_session.query(LocationModel).\
            filter_by(id=data['id'])
        Location.update(data)
        db_session.commit()
        Location = db_session.query(LocationModel).\
            filter_by(id=data['id']).first()

        return UpdateLocation(Location=Location)


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
    stateProvinceList = SQLAlchemyConnectionField(StateProvince)
    countryList = SQLAlchemyConnectionField(Country)
    locationList = SQLAlchemyConnectionField(Location)
    userList = SQLAlchemyConnectionField(User)
    hivesList = SQLAlchemyConnectionField(Hive)


class Mutation(graphene.ObjectType):
    createCountry = CreateCountry.Field()
    updateCountry = UpdateCountry.Field()
    createStateProvince = CreateStateProvince.Field()
    updateStateProvince = UpdateStateProvince.Field()
    createLocation = CreateLocation.Field()
    updateLocation = UpdateLocation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
