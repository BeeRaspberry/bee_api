import graphene
from graphene import (Mutation, Connection, InputObjectType, String,
                      Field, Boolean, Node)
from graphene_sqlalchemy import (SQLAlchemyObjectType)
from app.database import Location as LocationModel
from app import DB
from helpers import utils
from .helpers import TotalCount
from app.filters import FilterConnectionField
from .state_province import check_state_province


def check_location(data):
    result = DB.session.query(LocationModel). \
        filter_by(street_address=data['street_address'],
                  city=data['city']).first()
    if result is None:
        result = LocationModel(**data)
        DB.session.add(result)
        DB.session.commit()
    return result


class LocationAttribute:
    street_address = String(description="Street Address")
    city = String(description="City Location")
    postal_code = String(description="Zip or Postal Code")
    state_province = String(description="Name of state, province, ")


class LocationNode(SQLAlchemyObjectType):
    class Meta:
        model = LocationModel
        interfaces = (Node,)
        connection_field_factory = FilterConnectionField.factory


class LocationConnection(Connection):
    """ Location Connection """
    class Meta:
        """ Location Connection """
        node = LocationNode
        interfaces = (TotalCount,)


class CreateLocationInput(graphene.InputObjectType,
                          LocationAttribute):
    pass


class CreateLocation(Mutation):
    Location = Field(
        lambda: LocationNode,
        description="StateProvince created by this mutation.")

    class Arguments:
        input = CreateLocationInput(required=True)

    def mutate(self, info, input_value):
        data = utils.input_to_dictionary(input_value)
        state_data = {'name': input['state_province']}
        state_province = check_state_province(state_data)
        data['state_province'] = state_province

        return CreateLocation(Location=check_location(data))


class UpdateLocationInput(InputObjectType,
                          LocationAttribute):
    id = graphene.ID(required=True,
                     description="Global Id of the Location.")


class UpdateLocation(Mutation):
    Location = Field(lambda: LocationNode,
                     description="Location updated by this mutation.")

    class Arguments:
        input = UpdateLocationInput(required=True)

    def mutate(self, info, input_value):
        data = utils.input_to_dictionary(input_value)

        location = DB.session.query(LocationModel).\
            filter_by(id=data['id'])
        location.update(data)
        DB.session.commit()
        location = DB.session.query(LocationModel).\
            filter_by(id=data['id']).first()

        return UpdateLocation(Location=location)


class DeleteLocation(Mutation):
    ok = Boolean()

    class Arguments:
        input = UpdateLocationInput(required=True)

    def mutate(self, info, input_value):
        data = utils.input_to_dictionary(input_value)

        location = DB.session.query(LocationModel).filter_by(id=data['id'])
        location.delete()
        DB.session.commit()

        return DeleteLocation(ok=True)
