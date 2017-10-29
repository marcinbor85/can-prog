'''
Created on 23.10.2017

@author: Marcin Borowicz <marcinbor85@gmail.com>

'''

import intelhex

class FileManager(object):
    def __init__(self):
        self._ih = intelhex.IntelHex()
        
    def load(self, filename, fmt, address=0):
        if fmt == 'bin':
            self._ih.loadbin(filename, offset=address)
        elif fmt == 'hex':
            self._ih.loadhex(filename)
        else:
            raise ValueError('Unsupported file format type')
        
    def get_segments(self):
        for s in self._ih.segments():
            address = s[0]
            size = s[1]-address
            data = self._ih.tobinarray(start=address, size=size)
            yield (address, data,)
            
    def set_segment(self, address, data):
        for b in data:
            data = self._ih[address] = b
            address += 1
            
    def save(self, filename, fmt):
        if fmt == 'bin':
            self._ih.tobinfile(filename)
        elif fmt == 'hex':
            self._ih.write_hex_file(filename, write_start_addr=False)
        else:
            raise ValueError('Unsupported file format type')
