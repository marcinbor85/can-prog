
'''
Created on 23.10.2017

@author: mborowicz
'''

class AbstractFileManager(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
    
    def get_segments(self):
        return self._get_segments()
    
    def set_data(self):
        pass
        
    @property
    def size(self):
        return 0
        