'''
Created on 23.10.2017

@author: mborowicz
'''
from binascii import hexlify

class AbstractCAN(object):
    '''
    classdocs
    '''
    
    def __init__(self, *args, **kwargs):
        pass
    
    def open(self):
        raise Exception('not implemented yet')
    
    def close(self):
        raise Exception('not implemented yet')
    
    def send(self):
        raise Exception('not implemented yet')
    
    def recv(self):
        raise Exception('not implemented yet')
    
class CanFrame(object):
    def __init__(self, mid, data=None, dlc=None, remote=False, extended=False):
        self._is_remote = remote
        self._is_extended = extended
        
        if not isinstance(extended, bool):
            raise TypeError('extended field should be bool type')
        
        if not isinstance(mid, int):
            raise TypeError('message id field should be int type')
        
        if not extended:
            if mid > 0x7FF or mid < 0:
                raise ValueError('message id overrange')
        else:
            if mid > 0x1FFFFFFF or mid < 0:
                raise ValueError('message id overrange')
            
        self._mid = mid
        
        if not isinstance(remote, bool):
            raise TypeError('remote field should be bool type')
        
        if remote:
            if not isinstance(dlc, int):
                raise TypeError('dlc field should be int type')
            
            if dlc > 8 or dlc < 0:
                raise ValueError('dlc overrange')
            self._dlc = dlc
            self._data = None
        else:
            if not isinstance(data, bytes):
                raise TypeError('data field should be bytes type')
            
            self._dlc = len(data)
            if self.dlc > 8:
                raise ValueError('data field too long')
        
            self._data = data
        
    @property
    def is_remote(self):
        return self._is_remote     
    
    @property
    def is_extended(self):
        return self._is_extended
    
    @property
    def data(self):
        return self._data
    
    @property
    def mid(self):
        return self._mid
    
    @property
    def dlc(self):
        return self._dlc

    def __str__(self, *args, **kwargs):
        t = 'R' if self._is_remote else 'D'
        i = '{:08X}'.format(self.mid) if self._is_extended else '{:03X}'.format(self.mid)
        d = hexlify(self._data).decode('ascii').upper() if not self._is_remote else ''
        return 'CanFrame({type} {mid} {dlc} {data})'.format(type=t, mid=i, dlc=self._dlc, data=d)

    