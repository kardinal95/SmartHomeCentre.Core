from py.drivers.interface.models import InterfaceEpTypeEnum


class InterfaceEndpointHelper:
    if_parameters = {
        InterfaceEpTypeEnum.switch: {
            'state': int
        },
        InterfaceEpTypeEnum.rgb: {
            'code': str
        },
        InterfaceEpTypeEnum.display: {
            'state': None
        }
    }

    @staticmethod
    def get_all_types():
        return {x.name: x.value for x in InterfaceEpTypeEnum}