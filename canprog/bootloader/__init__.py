from .common import AbstractFileManager

from . import files

def get_file_manager_class_by_name(name):
    if name == 'hex':
        return files.HexFileManager
    elif name == 'bin':
        return files.BinFileManager
    else:
        raise NotImplementedError('unknown file format type')