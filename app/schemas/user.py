from graphene import (Mutation, Connection, InputObjectType, String,
                      Field, Boolean, Node, ID, Union, ObjectType)
from graphene_sqlalchemy import (SQLAlchemyObjectType)
from flask_graphql_auth import (create_access_token,
                                create_refresh_token,
                                get_jwt_identity,
                                AuthInfoField,
                                mutation_jwt_refresh_token_required,
                                GraphQLAuth)
from app.database import (User as UserModel,
                          Role, RolesUsers)
from app import (APP, DB)
from helpers.utils import input_to_dictionary
from .helpers import TotalCount
from app.filters import FilterConnectionField

auth = GraphQLAuth(APP)

user_claims = {"message": "VERI TAS LUX MEA"}


class MessageField(ObjectType):
    message = String()


class ProtectedUnion(Union):
    class Meta:
        types = (MessageField, AuthInfoField)

    @classmethod
    def resolve_type(cls, instance, info):
        return type(instance)


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


class LoginUser(Mutation):
    class Arguments(object):
        email = String()
        password = String()
        provider = String()

    access_token = String()
    refresh_token = String()
    role = String()
    name = String()

    @classmethod
    def mutate(cls, _, info, email, password, provider):
        if 'email' in provider:
            user = UserModel.query.filter_by(email=email).first()

        if 'google' in provider:
            print('need to implement Google Signin')
        if 'fb' in provider:
            print('need to implement Facebook signin')

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

        print('before create access token')
        access_token = create_access_token(email, user_claims=user_claims)
        refresh_token = create_refresh_token(email, user_claims=user_claims)
        print('access token: {}'.format(access_token))
        print('refresh token: {}'.format(refresh_token))

        return LoginUser(access_token=access_token,
                         refresh_token=refresh_token,
                         role=user_role,
                         name=user_name
                         )


class UserAttribute:
    email = String()
    firstName = String()
    lastName = String()
    password = String()
    phoneNumber = String()
    street_address = String(description="Street Address")
    city = String(description="City Location")
    postal_code = String(description="Zip or Postal Code")
    state_province = String(description="Name of state, province, ")


class UserNode(SQLAlchemyObjectType, UserAttribute):
    class Meta:
        model = UserModel
        interfaces = (Node,)
        connection_field_factory = FilterConnectionField.factory


class UserConnection(Connection):
    """ User Connection """
    class Meta:
        """ User Connection """
        node = UserNode
        interfaces = (TotalCount,)


class CreateUserInput(InputObjectType, UserAttribute):
    pass


class CreateUser(Mutation):
    user = Field(lambda: UserNode,
                 description="User created by this mutation.")

    class Arguments:
        input = CreateUserInput(required=True)

    def mutate(self, info, input_value):
        data = input_to_dictionary(input_value)

        user = UserModel(**data)
        DB.session.add(user)
        DB.session.commit()

        return CreateUser(user=user)


class UpdateUserInput(InputObjectType, UserAttribute):
    id = ID(required=True,
            description="Global Id of the User.")


class UpdateUser(Mutation):
    User = Field(lambda: UserNode,
                 description="User updated by this mutation.")

    class Arguments:
        input = UpdateUserInput(required=True)

    def mutate(self, info, input_value):
        data = input_to_dictionary(input_value)

        user = DB.session.query(UserModel).\
            filter_by(id=data['id'])
        user.update(data)
        DB.session.commit()
        user = DB.session.query(UserModel).\
            filter_by(id=data['id']).first()

        return UpdateUser(User=user)


class DeleteUser(Mutation):
    ok = Boolean()

    class Arguments:
        input = UpdateUserInput(required=True)

    def mutate(self, info, input_value):
        data = input_to_dictionary(input_value)

        user = DB.session.query(UserModel).filter_by(id=data['id'])
        user.delete()
        DB.session.commit()

        return DeleteUser(ok=True)
