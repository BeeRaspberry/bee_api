import graphene
from graphene import (relay, Mutation, String, Field, Node, ObjectType)
from flask_graphql_auth import mutation_jwt_required
from .schemas.country import (CountryNode, CountryConnection, CreateCountry,
                              DeleteCountry, UpdateCountry)
from .schemas.state_province import (StateProvinceNode, CreateStateProvince,
                                     StateProvinceConnection,
                                     UpdateStateProvince, DeleteStateProvince)
from .schemas.location import (LocationNode, LocationConnection,
                               CreateLocation, UpdateLocation, DeleteLocation)
from .schemas.user import (UserNode, UserConnection, CreateUser, UpdateUser,
                           DeleteUser, LoginUser, ProtectedUnion, MessageField)
from .filters import (FilterConnectionField)

#__all__ = ['CreateCountry', 'UpdateCountry', 'CreateLocation',
#           'UpdateLocation', 'CreateStateProvince', 'UpdateStateProvince',
#           'LoginUser']


def check_user(data):
    return True


class ProtectedMutation(Mutation):
    class Arguments(object):
        token = String()

    message = Field(ProtectedUnion)

    @classmethod
    @mutation_jwt_required
    def mutate(cls, _, info):
        return ProtectedMutation(message=MessageField(
                                 message="Protected mutation works"))


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


SCHEMA = graphene.Schema(query=Query, mutation=Mutation)
