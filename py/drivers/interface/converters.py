from py.drivers.interface.models import InterfaceEpTypeEnum


def convert(if_type: InterfaceEpTypeEnum, direction, parameters):
    converter = mapping[if_type]
    return converter(direction, parameters)


def rgb_converter(direction, parameters):
    def clamp(x):
        return max(0, min(x, 255))

    if direction == 'encode':
        code = "#{0:02x}{1:02x}{2:02x}".format(clamp(parameters['red']),
                                               clamp(parameters['green']),
                                               clamp(parameters['blue']))
        return {
            'code': code
        }


def switch_converter(direction, parameters):
    if direction == 'encode':
        return {
            'enabled': parameters['value']
        }


mapping = {
    InterfaceEpTypeEnum.switch: switch_converter,
    InterfaceEpTypeEnum.display: None,
    InterfaceEpTypeEnum.rgb: rgb_converter
}