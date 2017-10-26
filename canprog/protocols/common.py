'''
Created on 23.10.2017

@author: mborowicz
'''

class AbstractProtocol(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        
    def init(self):
        raise Exception('not implemented yet')
    
    def read_flash(self, address, size):
        raise Exception('not implemented yet')
    
    def write_flash(self, address, data):
        raise Exception('not implemented yet')
    
    def erase_flash(self):
        raise Exception('not implemented yet')
    
    def lock(self):
        raise Exception('not implemented yet')
    
    def unlock(self):
        raise Exception('not implemented yet')
    
    def go(self):
        raise Exception('not implemented yet')
    