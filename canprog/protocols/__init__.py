'''
Created on 23.10.2017

@author: Marcin Borowicz <marcinbor85@gmail.com>

'''

from .abstract import AbstractProtocol

from . import stm32

def get_protocol_class_by_name(name):
    if name == 'stm32':
        return stm32.STM32Protocol
    else:
        raise NotImplementedError('unknown protocol type')
