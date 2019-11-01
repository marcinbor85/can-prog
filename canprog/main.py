#!/usr/bin/python

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

import argparse
import can
import sys

from canprog import __version__, __appname__, __description__
from canprog import protocols
from canprog import file
from canprog.logger import log

import canprog.logger

def config_parser():

    parser = argparse.ArgumentParser(prog=__appname__, description=__description__)
    parser._optionals.title = 'others' 

    parser.add_argument('--verbose', action='store_true', default=False, help='enable verbose output')
    parser.add_argument('--version', action='version', version='%(prog)s {version}'.format(version=__version__))
    
    group = parser.add_argument_group('configuration')
    group.add_argument('-n', dest='name', action='store', default='slcan0', help='interface name (default: slcan0)')
    group.add_argument('-i', dest='interface', action='store', choices=('socketcan',), default='socketcan', help='interface type (default: socketcan)')
    group.add_argument('-f', dest='format', action='store', choices=('hex','bin'), default='hex', help='file format (default: hex)')
    
    subparsers = parser.add_subparsers(title='protocols', dest='protocol')
    
    subparsers.required = True
    
    parser_stm32 = subparsers.add_parser('stm32', help='STM32 ROM bootloader')
    parser_stm32._optionals.title = 'others' 
    
    subparsers_stm32 = parser_stm32.add_subparsers(title='commands', dest='command')
    subparsers_stm32.required = True
    
    parser_command = subparsers_stm32.add_parser('write', help='write file to target memory')
    parser_command._optionals.title = 'others' 
    group = parser_command.add_argument_group('options')
    group.add_argument('-e', dest='erase', action='store_true', default=False, help='erase memory before write')
    group.add_argument('-P', dest='pages', action='store', type=lambda x: int(x,0), default=[], nargs='+', help='list of pages to erase (default: all)')
    group.add_argument('-v', dest='verify', action='store_true', default=False, help='verify memory after write')
    group.add_argument('-g', dest='go', action='store_true', default=False, help='start application after write')
    group.add_argument('-a', dest='address', action='store', type=lambda x: int(x,0), default=0x08000000, help='start memory address (default: 0x08000000)')
    group = parser_command.add_argument_group('arguments')    
    group.add_argument('input', action='store', help='input filename')
    
    parser_command = subparsers_stm32.add_parser('read', help='read target memory to file')
    parser_command._optionals.title = 'others' 
    group = parser_command.add_argument_group('options')
    group.add_argument('-a', dest='address', action='store', type=lambda x: int(x,0), default=0x08000000, help='start memory address (default: 0x08000000)')
    group.add_argument('-s', dest='size', action='store', type=lambda x: int(x,0), default=0x8000, help='data size to read (default: 0x8000)')
    group = parser_command.add_argument_group('arguments')    
    group.add_argument('output', action='store', help='output filename')

    parser_command = subparsers_stm32.add_parser('erase', help='erase target memory')
    parser_command._optionals.title = 'others' 
    group = parser_command.add_argument_group('options')
    group.add_argument('-P', dest='pages', action='store', type=lambda x: int(x,0), default=[], nargs='+', help='list of pages to erase (default: all)')
    
    parser_command = subparsers_stm32.add_parser('go', help='start program application')
    parser_command._optionals.title = 'others' 
    group = parser_command.add_argument_group('options')
    group.add_argument('-a', dest='address', action='store', type=lambda x: int(x,0), default=0x08000000, help='start memory address (default: 0x08000000)')
    
    parser_command = subparsers_stm32.add_parser('lock', help='enable readout protection')
    parser_command = subparsers_stm32.add_parser('unlock', help='disable readout protection')

    parser_command = subparsers_stm32.add_parser('speed', help='change the can baud rate the boot rom uses')
    group = parser_command.add_argument_group('arguments')
    group.add_argument('bps', action='store', type=lambda x: int(x), help='new baud rate')

    """
    parser_simple = subparsers.add_parser('simple', help='Simple bootloader')
    parser_simple._optionals.title = 'others' 
     
    subparsers_simple = parser_simple.add_subparsers(title='commands', dest='command')
    
    subparsers_simple.required = True
    
    parser_command = subparsers_simple.add_parser('write', help='write file to target')
    group = parser_command.add_argument_group('read options')
    group.add_argument('input', action='store', help='input filename')
    """
    
    return parser

def connect(protocol):
    try:
        log.info('Connecting target')
        protocol.connect()          
        log.info('Connected')
    except TimeoutError as e:
        raise ConnectionError('Connecting error: '+str(e))

def disconnect(protocol):
    try:
        log.info('Disconnecting target')
        protocol.disconnect()
        log.info('Disconnected')
    except TimeoutError as e:
        raise ConnectionError('Disconnecting error: '+str(e))
    
def go(protocol, address):
    try:
        log.info('Starting application')
        protocol.go(address)
        log.info('Successful')
    except TimeoutError as e:
        raise ConnectionError('Starting error: '+str(e))
    
def erase(protocol, pages):
    try:
        log.info('Erasing memory. Please wait...')
        protocol.erase(pages)
        log.info('Successful')
    except TimeoutError as e:
        raise ConnectionError('Erasing error: '+str(e))

def read(protocol, address, size):
    try:
        log.info('Reading memory at 0x{address:08X}:{size}'.format(address=address, size=size))
        d = protocol.read(address, size)
        log.info('Successful')
        return d
    except TimeoutError as e:
        raise ConnectionError('Reading error: '+str(e))

def write(protocol, address, data):
    try:
        log.info('Writing memory at 0x{address:08X}:{size}'.format(address=address, size=len(data)))
        protocol.write(address, data)
        log.info('Successful')
    except TimeoutError as e:
        raise ConnectionError('Writing error: '+str(e))

def verify(protocol, address, data):
    try:
        log.info('Verifying memory at 0x{address:08X}:{size}'.format(address=address, size=len(data)))
        data_readed = protocol.read(address, len(data))
        if len(data_readed) != len(data):
            raise ValueError('Size mismatch {} != {}'.format(len(data_readed),len(data)))
        for (a, b), i in zip(zip(data_readed, data), range(address, address+len(data))):
            if a != b:
                raise ValueError('Mismatch at 0x{address:08X} 0x{:02X}!=0x{:02X}'.format(a, b, address=i))
        log.info('Successful')
    except TimeoutError as e:
        raise ConnectionError('Verifying error: '+str(e))
    except ValueError as e:
        raise ConnectionError('Verifying error: '+str(e))
    
def lock(protocol):
    try:
        log.info('Enabling readout protection')
        protocol.lock()          
        log.info('Successful')
    except TimeoutError as e:
        raise ConnectionError('Enabling error: '+str(e))

def unlock(protocol):
    try:
        log.info('Disabling readout protection')
        protocol.unlock()          
        log.info('Successful')
    except TimeoutError as e:
        raise ConnectionError('Disabling error: '+str(e))                      

def speed(protocol, bps):
    try:
        log.info('Setting speed to %d bps' % (bps,))
        protocol.speed(bps)
        log.info('Command sent')
    except TimeoutError as e:
        raise ConnectionError('Writing error: '+str(e))

def main():
    
    parser = config_parser()
    
    params = parser.parse_args()
    
    if params.verbose:
        canprog.logger.set_level(canprog.logger.logging.DEBUG)
    
    if params.interface == 'socketcan':
        iface = can.interface.Bus(channel=params.name, bustype='socketcan_native')
    
    datafile = file.FileManager()
    
    protocol_class = protocols.get_protocol_class_by_name(params.protocol)
    protocol = protocol_class(iface)
    
    try:
        connect(protocol)
        
        if params.command == 'go':
            go(protocol, params.address)
        elif params.command == 'erase':
            erase(protocol, params.pages)
        elif params.command == 'write':
            if params.erase:
                erase(protocol, params.pages)
            
            datafile.load(params.input, params.format, params.address)
            for address, data in datafile.get_segments():
                write(protocol, address, data)
                
            if params.verify:
                for address, data in datafile.get_segments():
                    verify(protocol, address, data)
                        
            if params.go:
                go(protocol, params.address)
        elif params.command == 'read':
            data = read(protocol, params.address, params.size)            
            datafile.set_segment(params.address, data)
            datafile.save(params.output, params.format)    
        elif params.command == 'lock':
            lock(protocol)
        elif params.command == 'unlock':
            unlock(protocol)            
        elif params.command == 'speed':
            speed(protocol, params.bps)
        else:
            log.info('Nothing to do...')
        
        disconnect(protocol)
        sys.exit(0)
    except ValueError as e:
        log.error(e)
    except ConnectionError as e:
        log.error(e)

if __name__ == '__main__':
    main()
    sys.exit(1)
    