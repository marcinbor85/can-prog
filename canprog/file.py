#
# The MIT License (MIT)
#
# Copyright (c) 2017 Marcin Borowicz <marcinbor85@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

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
