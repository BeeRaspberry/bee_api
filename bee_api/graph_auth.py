import graphene
from graphene import (ObjectType, String, Union, Mutation, Field)
from app import app
from database import User
from flask_graphql_auth import (AuthInfoField, GraphQLAuth, get_jwt_identity,
                                get_raw_jwt, create_access_token,
                                create_refresh_token, query_jwt_required,
                                mutation_jwt_refresh_token_required,
                                mutation_jwt_required)

auth = GraphQLAuth(app)
user_claims = {"message": "VERI TAS LUX MEA"}


class MessageField(ObjectType):
    message = String()


class ProtectedUnion(Union):
    class Meta:
        types = (MessageField, AuthInfoField)

    @classmethod
    def resolve_type(cls, instance, info):
        return type(instance)


class AuthMutation(Mutation):
    class Arguments(object):
        username = String()
        password = String()
        provider = String()

    access_token = String()
    refresh_token = String()

    @classmethod
    def mutate(self, info, username, password, provider):
        if 'email' in provider:
            user = User.query.filter_by(username=username,
                                        password=password).first()
            if not user:
                raise Exception('Authentication Failure: User is registered')
        if 'google' in provider:
            print('need to implement Google Signin')
        if 'fb' in provider:
            print('need to implement Facebook signin')

        return AuthMutation(access_token=create_access_token(username,
                            user_claims=user_claims),
                            refresh_token=create_refresh_token(username,
                            user_claims=user_claims))


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
    class Arguments(ob
        token = String()

    new_token = String()

    @classmethod
    @mutation_jwt_refresh_token_required
    def mutate(self, _, info):
        current_user = get_jwt_identity()
        return RefreshMutation(new_token=create_access_token(
            identity=current_user, user_claims=user_claims))


class Mutation(ObjectType):
    auth = AuthMutation.Field()
    refresh = RefreshMutation.Field()
    protected = ProtectedMutation.Field()


class Query(ObjectType):
    protected = Field(type=ProtectedUnion,
                      message=String(), token=String())

    @query_jwt_required
    def resolve_protected(self, info, message):
        return MessageField(message=str(get_raw_jwt()))
