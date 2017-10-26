'''
Created on 23.10.2017

@author: mborowicz
'''

from . import AbstractCAN

class SerialCAN(AbstractCAN):
    '''
    classdocs
    '''
    
    def __init__(self, params):
        super().__init__()
        