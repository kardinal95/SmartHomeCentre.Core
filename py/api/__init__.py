from dynaconf import settings
from flask import Flask
from flask_restful import Api
from py.api.client.resources.devices import *
from py.api.client.resources.rooms import *
from py.api.client.resources.users import *


class FlaskSrv:
    def __init__(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)

        self.app.config['SECRET_KEY'] = settings.FLASK_SECRET_KEY
        self.app.config['JWT_SECRET_KEY'] = settings.JWT_SECRET_KEY
        self.app.config['JWT_BLACKLIST_ENABLED'] = True
        self.app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
        self.jwt = JWTManager(self.app)

        @self.jwt.token_in_blacklist_loader
        def check_if_token_in_blacklist_loader(decrypted_token):
            jti = decrypted_token['jti']
            return token_is_revoked(jti)

        self.add_resources()

    def add_resources(self):
        self.api.add_resource(Rooms, '/api/client/rooms')
        self.api.add_resource(RoomDevices, '/api/client/rooms/<string:room_uuid>/devices')
        self.api.add_resource(RoomDevicesExtended, '/api/client/rooms/<string:room_uuid>/devices/extended')
        self.api.add_resource(Devices, '/api/client/devices')
        self.api.add_resource(Device, '/api/client/devices/<string:device_uuid>/')
        self.api.add_resource(DeviceExtended, '/api/client/devices/<string:device_uuid>/extended')
        self.api.add_resource(DeviceEndpoints, '/api/client/devices/<string:device_uuid>/endpoints')
        self.api.add_resource(DeviceEndpoint,
                              '/api/client/devices/<string:device_uuid>/endpoints/<string:endpoint_uuid>')
        self.api.add_resource(DeviceEndpointState,
                              '/api/client/devices/<string:device_uuid>/endpoints/<string:endpoint_uuid>/state')
        self.api.add_resource(UserLogin, '/api/client/auth/login')
        self.api.add_resource(TokenRefresh, '/api/client/auth/refresh')
        self.api.add_resource(UserLogoutRefresh, '/api/client/auth/refreshlogout')
        self.api.add_resource(UserLogoutAccess, '/api/client/auth/accesslogout')

    def run(self):
        # TODO Debug and other variables to settings

        self.app.run(debug=False)
