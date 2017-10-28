'''
Created on 23.10.2017

@author: mborowicz
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
            raise Exception('canbus interface not compatible')
        self._iface = iface
        
    def _send(self, msg):
        try:
            self._iface.send(msg)
            log.debug('TX: '+canframe_to_string(msg))
        except can.CanError:
            raise IOError('Sending error')
    
    def _recv(self, checker=None):
        time = current_time()
        response = None
        while current_time() - time < self.RECV_TIMEOUT:
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
            raise Exception('Connect method not implemented')
        except Exception as e:
            raise Exception('Connecting error: '+str(e))
    
    def disconnect(self):
        try:
            self._disconnect()
        except AttributeError as e:
            raise Exception('Disconnect method not implemented')
        except Exception as e:
            raise Exception('Disconnecting error: '+str(e))
    
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
    
    def go(self, address):
        try:
            self._go(address)
        except AttributeError as e:
            raise Exception('Go method not implemented')
        except Exception as e:
            raise Exception('Starting application error: '+str(e))
 