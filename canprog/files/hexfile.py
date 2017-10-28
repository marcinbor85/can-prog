'''
Created on 23.10.2017

@author: mborowicz
'''

from . import AbstractFileManager

import intelhex

class HexFileManager(AbstractFileManager):
    '''
    classdocs
    '''

    def __init__(self, filename, *args):
        self._ih = intelhex.IntelHex()
        self._ih.padding = 0xFF
        self._ih.loadhex(filename)
        
    def _get_segments(self):
        for s in self._ih.segments():
            address = s[0]
            size = s[1]-address
            data = self._ih.tobinarray(start=address, size=size)
            yield (address, data,)
