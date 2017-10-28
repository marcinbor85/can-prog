'''
Created on 23.10.2017

@author: mborowicz
'''

from canprog.canbus import AbstractCAN

class AbstractProtocol(object):
    '''
    classdocs
    '''


    def __init__(self, iface):
        if not isinstance(iface, AbstractCAN):
            raise Exception('canbus interface not compatible')
        self._iface = iface
        
    def connect(self):
        raise NotImplementedError('not implemented yet')
    
    def disconnect(self):
        raise NotImplementedError('not implemented yet')
    
    def read(self, address, size):
        raise NotImplementedError('not implemented yet')
    
    def write(self, address, data):
        raise NotImplementedError('not implemented yet')
    
    def erase(self):
        raise NotImplementedError('not implemented yet')
    
    def lock(self):
        raise NotImplementedError('not implemented yet')
    
    def unlock(self):
        raise NotImplementedError('not implemented yet')
    
    def go(self):
        raise NotImplementedError('not implemented yet')

    def info(self):
        raise NotImplementedError('not implemented yet')    