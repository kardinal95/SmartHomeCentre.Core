import os

from sqlalchemy import Column, String, Integer, Binary

from py.models import DatabaseModel
import hashlib


def _make_salt():
    return os.urandom(32)


class RevokedTokenMdl(DatabaseModel):
    __tablename__ = 'revoked_tokens'
    jti = Column(String(120))


class UserMdl(DatabaseModel):
    __tablename__ = 'users'
    username = Column(String(64), unique=True)
    passhash = Column(Binary(32), nullable=False)
    salt = Column(Binary(32), nullable=False)
    acl = Column(Integer)

    def set_password(self, password, salt=None):
        if salt is None:
            salt = _make_salt()
        key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000
        )

        self.salt = salt
        self.passhash = key

    def verify_password(self, password):
        key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            self.salt,
            100000
        )
        if key == self.passhash:
            return True
        return False
