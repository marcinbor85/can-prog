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

import can 
import sys
import time

from canprog.logger import log

if 'win' in sys.platform.lower():
    current_time = time.clock
else:
    current_time = time.time
    
def canframe_to_string(msg):

    array = []
    
    flags = ''
    if msg.is_remote_frame:
        flags += 'R'
    if msg.is_error_frame:
        flags += 'E'
        
    if flags != '':
        array.append(flags)
    
    if msg.is_extended_id:
        aid = '{:08X}'.format(msg.arbitration_id)
    else:
        aid = '{:03X}'.format(msg.arbitration_id)
        
    array.append(aid)
    array.append(str(msg.dlc))

    data = ''.join(['{:02X}'.format(b) for b in msg.data])
    
    if data != '':
        array.append(data)

    return ':'.join(array)
    
class AbstractProtocol(object):
    '''
    classdocs
    '''
    RECV_TIMEOUT = 1.0

    def __init__(self, iface):
        if not isinstance(iface, can.BusABC):
            raise TypeError('canbus interface not compatible')
        self._iface = iface
        
    def _send(self, msg):
        try:
            self._iface.send(msg)
            log.debug('TX: '+canframe_to_string(msg))
        except can.CanError:
            raise IOError('Sending error')
    
    def _recv(self, timeout=None, checker=None):
        if timeout == None:
            t = self.RECV_TIMEOUT
        else:
            t = timeout
        time = current_time()
        response = None
        while current_time() - time < t:
            frame = self._iface.recv(0.0)
            if frame:
                if checker != None:
                    if not checker(frame):
                        continue                
                response = frame
                break

        if not response:
            raise TimeoutError('Receiving timeout')
        
        log.debug('RX: '+canframe_to_string(response))
        return response
        
    def connect(self):
        try:
            self._connect()
        except AttributeError as e:
            raise NotImplementedError('Connect method not implemented')
    
    def disconnect(self):
        try:
            self._disconnect()
        except AttributeError as e:
            raise NotImplementedError('Disconnect method not implemented')
    
    def read(self, address, size):
        try:
            return self._read(address, size)
        except AttributeError as e:
            raise NotImplementedError('Read method not implemented')
    
    def write(self, address, data):
        try:
            self._write(address, data)
        except AttributeError as e:
            raise NotImplementedError('Write method not implemented')
    
    def erase(self, pages):
        try:
            self._erase(pages)
        except AttributeError as e:
            raise NotImplementedError('Erase method not implemented')
        
    def lock(self):
        try:
            self._lock()
        except AttributeError as e:
            raise NotImplementedError('Lock method not implemented')
    
    def unlock(self):
        try:
            self._unlock()
        except AttributeError as e:
            raise NotImplementedError('Unlock method not implemented')
    
    def go(self, address):
        try:
            self._go(address)
        except AttributeError as e:
            raise NotImplementedError('Go method not implemented')

    def speed(self, bps):
        try:
            self._speed(bps)
        except AttributeError as e:
            raise NotImplementedError('Speed method not implemented')
