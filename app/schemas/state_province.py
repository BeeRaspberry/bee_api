import graphene
from graphene import (Mutation, Connection, InputObjectType, String,
                      Field, Boolean, Node)
from graphene_sqlalchemy import (SQLAlchemyObjectType)
from app.database import StateProvince as StateProvinceModel
from app import DB
from helpers.utils import input_to_dictionary
from .helpers import TotalCount
from app.filters import FilterConnectionField


def check_state_province(data):
    result = DB.session.query(StateProvinceModel). \
        filter_by(name=data['name']).first()
    if result is None:
        result = StateProvinceModel(**data)
        DB.session.add(result)
        DB.session.commit()
    return result


class StateProvinceAttribute:
    name = String(
      description="Name of the State, Province, or Region.")
    country = String(
      description="Assign State, Province, or Region to this Country.")


class StateProvinceNode(SQLAlchemyObjectType):
    class Meta:
        model = StateProvinceModel
        interfaces = (Node,)
        connection_field_factory = FilterConnectionField.factory


class StateProvinceConnection(Connection):
    """ StateProvince Connection """
    class Meta:
        """ StateProvince Connection """
        node = StateProvinceNode
        interfaces = (TotalCount,)


class CreateStateProvinceInput(InputObjectType,
                               StateProvinceAttribute):
    pass


class CreateStateProvince(Mutation):
    StateProvince = Field(
      lambda: StateProvinceNode,
      description="StateProvince created by this mutation.")

    class Arguments:
        input = CreateStateProvinceInput(required=True)

    def mutate(self, info, input_value):
        data = input_to_dictionary(input_value)

        return CreateStateProvince(StateProvince=check_state_province(data))


class UpdateStateProvinceInput(InputObjectType,
                               StateProvinceAttribute):
    id = graphene.ID(required=True,
                     description="Global Id of the StateProvince.")


class UpdateStateProvince(Mutation):
    StateProvince = Field(
      lambda: StateProvinceNode,
      description="StateProvince updated by this mutation.")

    class Arguments:
        input = UpdateStateProvinceInput(required=True)

    def mutate(self, info, input_value):
        data = input_to_dictionary(input_value)

        state_province = DB.session.query(StateProvinceModel).\
            filter_by(id=data['id'])
        state_province.update(data)
        DB.session.commit()
        state_province = DB.session.query(StateProvinceModel).\
            filter_by(id=data['id']).first()

        return UpdateStateProvince(StateProvince=state_province)


class DeleteStateProvince(Mutation):
    ok = Boolean()

    class Arguments:
        input = UpdateStateProvinceInput(required=True)

    def mutate(self, info, input_value):
        data = input_to_dictionary(input_value)

        province = DB.session.query(StateProvinceModel).filter_by(id=data['id'])
        province.delete()
        DB.session.commit()

        return DeleteStateProvince(ok=True)
