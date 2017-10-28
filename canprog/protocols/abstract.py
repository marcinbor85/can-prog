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
    
class AbstractProtocol(object):
    '''
    classdocs
    '''

    def __init__(self, iface):
        if not isinstance(iface, can.BusABC):
            raise Exception('canbus interface not compatible')
        self._iface = iface
        
    def _send(self, msg):
        try:
            self._iface.send(msg)
            log.debug('TX: '+str(msg))
        except can.CanError:
            raise IOError('Sending error')
    
    def _recv(self, timeout=1.0, checker=None):
        timeout = 1.0
        time = current_time()
        response = None
        while current_time() - time < timeout:
            frame = self._iface.recv(0.0)
            if frame:
                if checker != None:
                    if not checker(frame):
                        continue                
                response = frame
                break

        if not response:
            raise TimeoutError('Receiving timeout')
        
        log.debug('RX: '+str(response))
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
 