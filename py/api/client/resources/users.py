from flask_jwt_extended import *
from flask_restful import Resource, reqparse, abort

from py.api.client.operations.users import *

parser = reqparse.RequestParser()
parser.add_argument('username', help='This field cannot be blank', required=True)
parser.add_argument('password', help='This field cannot be blank', required=True)


class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()
        user = get_user_by_username(data['username'])

        if user is None:
            abort(404, message='Incorrect user/password')

        if user.verify_password(data['password']):
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        else:
            abort(404, message='Incorrect user/password')


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        user = get_jwt_identity()
        access_token = create_access_token(identity=user)
        return {
            'access_token': access_token
        }


class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        revoke_token(jti)


class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        revoke_token(jti)