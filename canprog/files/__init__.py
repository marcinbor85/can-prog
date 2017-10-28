from .common import AbstractFileManager

from . import hexfile
from . import binfile

def get_file_manager_class_by_name(name):
    if name == 'hex':
        return hexfile.HexFileManager
    elif name == 'bin':
        return binfile.BinFileManager
    else:
        raise NotImplementedError('unknown file format type')