'''
Created on 23.10.2017

@author: Marcin Borowicz <marcinbor85@gmail.com>

'''

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
 