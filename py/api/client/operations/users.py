from py.core import MainHub
from py.core.db import DatabaseSrv
from py.models.user import UserMdl, RevokedTokenMdl


def get_user_by_username(username):
    session = MainHub.retrieve(DatabaseSrv).session()
    user = session.query(UserMdl).filter(UserMdl.username == username).first()
    session.close()

    return user


def revoke_token(jti):
    session = MainHub.retrieve(DatabaseSrv).session()
    session.add(RevokedTokenMdl(jti=jti))
    session.commit()
    session.close()


def token_is_revoked(jti):
    session = MainHub.retrieve(DatabaseSrv).session()
    token = session.query(RevokedTokenMdl).filter(RevokedTokenMdl.jti == jti).first()
    session.close()

    if token is None:
        return False
    return True


def get_user_acl(username):
    session = MainHub.retrieve(DatabaseSrv).session()
    user = session.query(UserMdl).filter(UserMdl.username == username).first()
    session.close()

    return user.acl
