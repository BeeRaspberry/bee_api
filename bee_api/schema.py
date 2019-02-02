import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField
from classes.country.schema \
    import (Country, CreateCountry, UpdateCountry)
from classes.user.schema import (User)
from classes.hive.schema import (Hive)
from classes.state_province.schema \
    import (StateProvince, CreateStateProvince,  UpdateStateProvince)
from classes.location.schema\
    import Location, CreateLocation, UpdateLocation
from classes.auth.schema import Auth, CheckAuth


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
    checkAuth = CheckAuth.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
