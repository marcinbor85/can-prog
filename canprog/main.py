'''
Created on 23.10.2017

@author: mborowicz
'''

import argparse
import sys

from canprog import __version__, __appname__

from canprog.logger import log

import canprog.logger
import logging

from canprog import protocols

import can

def config_parser():
    parser = argparse.ArgumentParser(prog=__appname__, description='Command-line tool to flashing devices by CAN-BUS', add_help=False)

    config = parser.add_argument_group('Configuration')
    config.add_argument('-n','--name', action='store', default='slcan0', help='interface name (default: slcan0)')
    config.add_argument('-i','--interface', action='store', choices=('socketcan',), default='socketcan', help='interface type (default: socketcan)')
    config.add_argument('-p','--protocol', action='store', choices=('stm32',), default='stm32', help='bootloader protocol (default: stm32)')
    config.add_argument('-f','--format', action='store', choices=('hex','bin'), default='hex', help='file format (default: hex)')
    config.add_argument('-c','--config', action='store', default=None, help='optional configuration file')
    
    config_write = parser.add_argument_group('Write options')    
    config_write.add_argument('-e','--erase', action='store_true', default=False, help='erase memory before write')
    config_write.add_argument('-v','--verify', action='store_true', default=False, help='verify memory after write')
    
    config_read = parser.add_argument_group('Read options')
    config_read.add_argument('-s','--size', action='store', type=lambda x: int(x,0), default=0x8000, help='data size to read (default: 0x8000)')
    
    config_readwrite = parser.add_argument_group('Read/Write/Go options')
    config_readwrite.add_argument('-a','--address', action='store', type=lambda x: int(x,0), default=0x08000000, help='start memory address (default: 0x08000000)')
    
    others = parser.add_argument_group('Others options')
    others.add_argument('-h','--help', action='help', help='show this help message and exit')
    others.add_argument('--verbose', action='store_true', default=False, help='enable verbose output')
    others.add_argument('--version', action='version', version='%(prog)s {version}'.format(version=__version__))

    parser_commands = parser.add_subparsers(title='Target commands',
                                       description='Supported target operations',
                                       dest='command')
     
    parser_write = parser_commands.add_parser('write', help='write file to target', add_help=False)
    config_write = parser_write.add_argument_group('write options')
    config_write.add_argument('input', action='store', help='input filename')

    parser_read = parser_commands.add_parser('read', help='read target to file', add_help=False)
    config_read = parser_read.add_argument_group('read options')
    config_read.add_argument('output', action='store', help='output filename')

    parser_commands.add_parser('erase', help='erase target memory', add_help=False)
    parser_commands.add_parser('go', help='go program application', add_help=False)
    parser_commands.add_parser('lock', help='enable readout protection', add_help=False)
    parser_commands.add_parser('unlock', help='disable readout protection', add_help=False)

    return parser

def main():
    
    parser = config_parser()
    
    params = parser.parse_args()
    
    if params.verbose:
        canprog.logger.set_level(logging.DEBUG)
    
    if params.interface == 'socketcan':
        iface = can.interface.Bus(channel=params.name, bustype='socketcan_native')
    
    try:
        protocol_class = protocols.get_protocol_class_by_name(params.protocol)
    except NotImplementedError as e:
        parser.error(e)
        
    protocol = protocol_class(iface)
    
    try:
        log.info('Trying to connect target')
        protocol.connect()          
        log.info('Connected')
        
        
        if params.command == 'go':
            log.info('Trying to start application')
            protocol.go(params.address)
            log.info('Starting successfull')
        elif params.command == 'erase':
            log.info('Trying to erase memory. Please wait...')
            protocol.erase()
            log.info('Erasing successfull')
        else:
            log.info('Nothing to do...')
            
        #protocol.erase()
        
        log.info('Trying to disconnect target')
        protocol.disconnect()
        log.info('Disconnected')
    except Exception as e:
        log.error(e)
        sys.exit(-1)

if __name__ == '__main__':
    main()