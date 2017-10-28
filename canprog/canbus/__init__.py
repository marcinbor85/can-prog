from .common import CanFrame, AbstractCAN

from . import socketcan

def get_can_interface_class_by_name(name):
    if name == 'socketcan':
        return socketcan.SocketCAN
    else:
        raise NotImplementedError('unknown can interface type')
