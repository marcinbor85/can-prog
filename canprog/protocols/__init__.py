from canprog.protocols.abstract import AbstractProtocol

from . import stm32

def get_protocol_class_by_name(name):
    if name == 'stm32':
        return stm32.STM32Protocol
    else:
        raise NotImplementedError('unknown protocol type')
