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
    country = db_session.query(CountryModel). \
        filter_by(name=data['country']).first()
    if country is None:
        country = CountryModel(data['country'])
        db_session.add(country)
        db_session.commit()
    return country


def check_state_province(data):
    state_province = db_session.query(StateProvinceModel). \
        filter_by(name=data['name']).first()
    if state_province is None:
        state_province = StateProvinceModel(**data)
        db_session.add(state_province)
        db_session.commit()
    return state_province



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
        country = check_country(data)
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


schema = graphene.Schema(query=Query, mutation=Mutation)
