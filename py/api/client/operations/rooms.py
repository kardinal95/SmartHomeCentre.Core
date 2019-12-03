from py.core import MainHub
from py.core.db import DatabaseSrv
from py.models.room import RoomMdl


def get_all_rooms():
    session = MainHub.retrieve(DatabaseSrv).session()
    rooms = session.query(RoomMdl).all()
    session.close()

    return rooms


def get_room(uuid):
    session = MainHub.retrieve(DatabaseSrv).session()
    room = session.query(RoomMdl).filter(RoomMdl.uuid == uuid).first()
    session.close()

    return room
