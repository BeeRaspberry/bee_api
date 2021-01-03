import graphene
from graphene import relay
from graphene_sqlalchemy import (SQLAlchemyObjectType,
                                 SQLAlchemyConnectionField)
from flask_graphql_auth import (AuthInfoField, GraphQLAuth, get_jwt_identity,
                                get_raw_jwt, create_access_token,
                                create_refresh_token, query_jwt_required,
                                mutation_jwt_refresh_token_required,
                                mutation_jwt_required)

from helpers import utils

from app import (app, db)
from .database import (Country as CountryModel, Location as LocationModel,
                       StateProvince as StateProvinceModel, Hive as HiveModel,
                       HiveData as HiveDataModel, User as UserModel,
                       Role, RolesUsers)

__all__ = ['CreateCountry', 'UpdateCountry', 'CreateLocation',
           'UpdateLocation', 'CreateStateProvince', 'UpdateStateProvince',
           'LoginUser']

auth = GraphQLAuth(app)
user_claims = {"message": "VERI TAS LUX MEA"}


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


class MessageField(graphene.ObjectType):
    message = graphene.String()


class ProtectedUnion(graphene.Union):
    class Meta:
        types = (MessageField, AuthInfoField)

    @classmethod
    def resolve_type(cls, instance, info):
        return type(instance)


class LoginUser(graphene.Mutation):
    class Arguments(object):
        email = graphene.String()
        password = graphene.String()
        provider = graphene.String()

    access_token = graphene.String()
    refresh_token = graphene.String()
    role = graphene.String()
    name = graphene.String()

    @classmethod
    def mutate(cls, _, info, email, password, provider):
        if 'email' in provider:
            user = UserModel.query.filter_by(email=email).first()

        if 'google' in provider:
            print('need to implement Google Signin')
        if 'fb' in provider:
            print('need to implement Facebook signin')

        print(user.password)
        print(password)
        if not user or user.password != password:
            raise Exception('Invalid Credentials')

        user_name = None
        if user.firstName or user.lastName:
            user_name = "{} {}".format(user.firstName, user.lastName).strip()
        else:
            user_name = user.email

        role = Role.query.join(RolesUsers).filter(user.id == user.id).first()
        if not role:
            user_role = 'user'
        else:
            user_role = role.name

        return LoginUser(access_token=create_access_token(email,
                         user_claims=user_claims),
                         refresh_token=create_refresh_token(email,
                         user_claims=user_claims),
                         role=user_role,
                         name=user_name
                        )


class ProtectedMutation(graphene.Mutation):
    class Arguments(object):
        token = graphene.String()

    message = graphene.Field(ProtectedUnion)

    @classmethod
    @mutation_jwt_required
    def mutate(cls, _, info):
        return ProtectedMutation(message=MessageField(
                                 message="Protected mutation works"))


class RefreshMutation(graphene.Mutation):
    class Arguments(object):
        token = graphene.String()

    new_token = graphene.String()

    @classmethod
    @mutation_jwt_refresh_token_required
    def mutate(self, _, info):
        current_user = get_jwt_identity()
        return RefreshMutation(new_token=create_access_token(identity=current_user, user_claims=user_claims))


class UserAttribute:
    email = graphene.String()
    firstName = graphene.String()
    lastName = graphene.String()
    password = graphene.String()
    phoneNumber = graphene.String()
    street_address = graphene.String(description="Street Address")
    city = graphene.String(description="City Location")
    postal_code = graphene.String(description="Zip or Postal Code")
    state_province = graphene.String(description="Name of state, province, ")


class User(SQLAlchemyObjectType, UserAttribute):
    class Meta:
        model = UserModel
        interfaces = (relay.Node, )


class CreateUserInput(graphene.InputObjectType, UserAttribute):
    pass


class CreateUser(graphene.Mutation):
    user = graphene.Field(lambda: User,
                             description="User created by this mutation.")

    class Arguments:
        input = CreateUserInput(required=True)

    def mutate(self, info, input_value):
        data = utils.input_to_dictionary(input_value)

        user = UserModel(**data)
        db.session.add(user)
        db.session.commit()

        return CreateUser(user=user)


class UpdateUserInput(graphene.InputObjectType,
                               UserAttribute):
    id = graphene.ID(required=True,
                     description="Global Id of the User.")


class UpdateUser(graphene.Mutation):
    User = graphene.Field(lambda: User,
                    description="User updated by this mutation.")

    class Arguments:
        input = UpdateUserInput(required=True)

    def mutate(self, info, input_value):
        data = utils.input_to_dictionary(input_value)

        user = db.session.query(UserModel).\
            filter_by(id=data['id'])
        user.update(data)
        db.session.commit()
        user = db.session.query(UserModel).\
            filter_by(id=data['id']).first()

        return UpdateUser(User=user)


class DeleteUser(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        input = UpdateUserInput(required=True)

    def mutate(self, info, input_value):
        data = utils.input_to_dictionary(input_value)

        user = db.session.query(UserModel).filter_by(id=data['id'])
        user.delete()
        db.session.commit()

        return DeleteUser(ok=True)


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
    createUser = CreateUser.Field()
    updateUser = UpdateUser.Field()
    deleteUser = DeleteUser.Field()
    loginUser = LoginUser.Field()
    refresh = RefreshMutation.Field()
    protected = ProtectedMutation.Field()
#    checkAuth = CheckAuth.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
