from py import db_session
from py.api.exceptions import IncorrectTargetException
from py.models.room import RoomMdl


@db_session
def get_all_rooms(session):
    return RoomMdl.get_all_rooms(session=session)


@db_session
def get_room(uuid, session):
    room = RoomMdl.get_room_with_uuid(uuid=uuid, session=session)
    if room is None:
        raise IncorrectTargetException(uuid, RoomMdl)
    return RoomMdl.get_room_with_uuid(uuid=uuid, session=session)
