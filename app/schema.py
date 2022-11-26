import graphene
from graphene import (relay, Mutation, String, Field, Node, ObjectType,
                      Union)
from flask_graphql_auth import (AuthInfoField, GraphQLAuth, get_jwt_identity,
                                get_raw_jwt, create_access_token,
                                query_jwt_required,
                                mutation_jwt_refresh_token_required,
                                mutation_jwt_required)
from app import app
from .schemas.country import (CountryNode, CountryConnection, CreateCountry,
                              DeleteCountry, UpdateCountry)
from .schemas.state_province import (StateProvinceNode, CreateStateProvince,
                                     StateProvinceConnection,
                                     UpdateStateProvince, DeleteStateProvince)
from .schemas.location import (LocationNode, LocationConnection,
                               CreateLocation, UpdateLocation, DeleteLocation)
from .schemas.user import (UserNode, UserConnection, CreateUser, UpdateUser,
                           DeleteUser, LoginUser)
from .filters import (FilterConnectionField)

__all__ = ['CreateCountry', 'UpdateCountry', 'CreateLocation',
           'UpdateLocation', 'CreateStateProvince', 'UpdateStateProvince',
           'LoginUser']

auth = GraphQLAuth(app)
user_claims = {"message": "VERI TAS LUX MEA"}


def check_user(data):
    return True


class MessageField(ObjectType):
    message = String()


class ProtectedUnion(Union):
    class Meta:
        types = (MessageField, AuthInfoField)

    @classmethod
    def resolve_type(cls, instance, info):
        return type(instance)



class ProtectedMutation(Mutation):
    class Arguments(object):
        token = String()

    message = Field(ProtectedUnion)

    @classmethod
    @mutation_jwt_required
    def mutate(cls, _, info):
        return ProtectedMutation(message=MessageField(
                                 message="Protected mutation works"))


class RefreshMutation(Mutation):
    class Arguments(object):
        token = String()

    new_token = String()

    @classmethod
    @mutation_jwt_refresh_token_required
    def mutate(self, _, info):
        current_user = get_jwt_identity()
        return RefreshMutation(new_token=create_access_token(
            identity=current_user, user_claims=user_claims))


class Query(ObjectType):
    node = relay.Node.Field()
    country = Node.Field(CountryNode)
    state_province = Node.Field(StateProvinceNode)
    location = Node.Field(LocationNode)
    user = Node.Field(UserNode)
    all_country = FilterConnectionField(CountryConnection)
    all_state_province = FilterConnectionField(StateProvinceConnection)
    all_location = FilterConnectionField(LocationConnection)
    all_user = FilterConnectionField(UserConnection)
    getStateProvinceCountry = Field(lambda: StateProvinceNode, country=String())
    def resolve_getStateProvinceCountry(parent, info, country):
        query = StateProvinceNode.get_query(info)
        return query.filter(country_id==country).first()
#    hivesList = SQLAlchemyConnectionField(Hive)


class Mutation(ObjectType):
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
#    refresh = RefreshMutation.Field()
#    protected = ProtectedMutation.Field()
#    checkAuth = CheckAuth.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
