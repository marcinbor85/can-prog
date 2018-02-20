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
import struct

from . import AbstractProtocol

from canprog.logger import log

CMD_GET_COMMANDS = 0x00
CMD_GET_VERSION = 0x01
CMD_GET_ID = 0x02
CMD_CHANGE_SPEED = 0x03
CMD_READ_MEMORY = 0x11
CMD_GO = 0x21
CMD_WRITE_MEMORY = 0x31
CMD_ERASE = 0x43
CMD_WRITE_PROTECT = 0x63
CMD_WRITE_UNPROTECT = 0x73
CMD_READOUT_PROTECT = 0x82
CMD_READOUT_UNPROTECT = 0x92

MASSERASE_MAX_TIMEOUT = 30.0
UNPROTECT_MAX_TIMEOUT = 2.0

BYTE_ACK = 0x79
BYTE_NOACK = 0x1F
BYTE_INIT = 0x79
BYTE_DATA = 0x04

CHIP_ID = { 0x440: "STM32F05xxx & STM32F030x8",
            0x444: "STM32F03xx4/6",
            0x442: "STM32F030xC",
            0x445: "STM32F04xxx & STM32F070x6",
            0x448: "STM32F070xB & STM32F071xx/072xx",
            0x442: "STM32F09xxx",
            
            0x412: "STM32F10xxx Low-density",
            0x410: "STM32F10xxx Medium-density",
            0x414: "STM32F10xxx High-density",
            0x420: "STM32F10xxx Medium-density VL",
            0x428: "STM32F10xxx High-density VL",
            0x418: "STM32F105xx/107xx",
            0x430: "STM32F10xxx XL-density",
            
            0x411: "STM32F2xxxx",
            
            0x432: "STM32F373xx & STM32F378xx",
            0x422: "STM32F302xB(C)/303xB(C) & STM32F358xx",
            0x439: "STM32F301xx/302x4(6/8) & STM32F318xx",
            0x438: "STM32F303x4(6/8)/334xx/328xx",
            0x446: "STM32F302xD(E)/303xD(E) & STM32F398xx",
            
            0x413: "STM32F40xxx/41xxx",
            0x419: "STM32F42xxx/43xxx",
            0x423: "STM32F401xB(C)",
            0x433: "STM32F401xD(E)",
            0x458: "STM32F410xx",
            0x431: "STM32F411xx",
            0x441: "STM32F412xx",
            0x421: "STM32F446xx",
            0x434: "STM32F469xx/479xx",
            0x463: "STM32F413xx/423xx",
            
            0x452: "STM32F72xxx/73xxx",
            0x449: "STM32F74xxx/75xxx",
            0x451: "STM32F76xxx/77xxx",
            
            0x450: "STM32H74xxx/75xxx",
            
            0x457: "STM32L01xxx/02xxx",
            0x425: "STM32L031xx/041xx",
            0x417: "STM32L05xxx/06xxx",
            0x447: "STM32L07xxx/08xxx",
            0x416: "STM32L1xxx6(8/B)",
            0x429: "STM32L1xxx6(8/B)A",
            0x427: "STM32L1xxxC",
            0x436: "STM32L1xxxD",
            0x437: "STM32L1xxxE",
            
            0x435: "STM32L43xxx/44xxx",
            0x462: "STM32L45xxx/46xxx",
            0x415: "STM32L47xxx/48xxx",
            0x461: "STM32L496xx/4A6xx",} 

def _check_support(cmd):
    def func_wrapper(function):
        def call_wrapper(*args):
            stm32 = args[0]
            command = stm32._supported_commands[cmd]
            if not command['support']:
                raise NotImplementedError('No support {name} command'.format(name=command['name']))
            return function(*args)
        return call_wrapper
    return func_wrapper

class STM32Protocol(AbstractProtocol):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._supported_commands = {  CMD_GET_COMMANDS: {'name': 'GET', 'support': False},
                                      CMD_GET_VERSION: {'name': 'GET_VERSION', 'support': False},
                                      CMD_GET_ID: {'name': 'GET_ID', 'support': False},
                                      CMD_CHANGE_SPEED: {'name': 'CHANGE_SPEED', 'support': False},
                                      CMD_READ_MEMORY: {'name': 'READ_MEMORY', 'support': False},
                                      CMD_GO: {'name': 'GO', 'support': False},
                                      CMD_WRITE_MEMORY: {'name': 'WRITE_MEMORY', 'support': False},
                                      CMD_ERASE: {'name': 'ERASE', 'support': False},
                                      CMD_WRITE_PROTECT: {'name': 'WRITE_PROTECT', 'support': False},
                                      CMD_WRITE_UNPROTECT: {'name': 'WRITE_UNPROTECT', 'support': False},
                                      CMD_READOUT_PROTECT: {'name': 'READOUT_PROTECT', 'support': False},
                                      CMD_READOUT_UNPROTECT: {'name': 'READOUT_UNPROTECT', 'support': False} }
    
    def _check_response(self, arb_id, dlc=None, ack_bytes=None):
        def _check_message(msg):
            if msg.arbitration_id != arb_id:
                return False
            if dlc:
                if msg.dlc != dlc:
                    return False
            if ack_bytes:
                if msg.data[0] in ack_bytes:
                    return True
                return False
            return True
        return _check_message
    
    def _check_ack(self, arb_id):
        return self._check_response(arb_id, 1, (BYTE_ACK,))
    
    def _check_byte(self, arb_id):
        return self._check_response(arb_id, 1)
    
    def _check_ack_or_noack(self, arb_id):
        return self._check_response(arb_id, 1, (BYTE_ACK, BYTE_NOACK))
    
    def _wait_for_ack(self, cmd, timeout=None):
        self._recv(timeout=timeout, checker=self._check_ack(cmd))
        
    def _send_data(self, cmd, data=[]):
        self._send(can.Message(arbitration_id=cmd, data=data, extended_id=False))
    
    def _init(self):
        self._send_data(BYTE_INIT)
        self._recv(checker=self._check_ack_or_noack(BYTE_INIT))
        
    def _recv_data(self, cmd, size=None):
        msg = self._recv(checker=self._check_response(cmd, size))
        return msg.data
        
    def _get_commands(self):
        self._send_data(CMD_GET_COMMANDS)

        self._wait_for_ack(CMD_GET_COMMANDS)
        commands_num = self._recv_data(CMD_GET_COMMANDS, 1)[0]
        boot_version = self._recv_data(CMD_GET_COMMANDS, 1)[0]
        
        commands = []
        for _ in range(commands_num):
            cmd = self._recv_data(CMD_GET_COMMANDS, 1)[0]
            commands.append(cmd)
            
        self._wait_for_ack(CMD_GET_COMMANDS)

        for k, v in self._supported_commands.items():
            v['support'] = True if k in commands else False

        self._bootloader_version = '{}.{}'.format((boot_version>>4)&0x0F, (boot_version)&0x0F)
    
    @_check_support(CMD_GET_VERSION)
    def _get_version(self):

        self._send_data(CMD_GET_VERSION)

        self._wait_for_ack(CMD_GET_VERSION)
        self._recv_data(CMD_GET_VERSION, 1)
        option_msg = self._recv_data(CMD_GET_VERSION, 2)[0:2]
        
        self._wait_for_ack(CMD_GET_VERSION)
        
        self._read_protection_bytes = '0x{}'.format(''.join(['{:02X}'.format(i) for i in option_msg]))
    
    @_check_support(CMD_GET_ID)
    def _get_id(self):
        self._send_data(CMD_GET_ID)

        self._wait_for_ack(CMD_GET_ID)
        chip_id = self._recv_data(CMD_GET_ID)
        self._wait_for_ack(CMD_GET_ID)
        
        self._chip_id = '0x{}'.format(''.join(['{:02X}'.format(i) for i in chip_id]))
        
    def _connect(self):
        self._init()
        log.info('Bootloader initialized')
        
        self._get_commands()       
                
        log.info('Bootloader version: {version}'.format(version=self._bootloader_version))
        
        try:
            self._get_version()                
            log.info('Read protection: {bytes}'.format(bytes=self._read_protection_bytes))
        except NotImplementedError as e:
            pass
        
        try:
            self._get_id()
            
            try:
                name = CHIP_ID[int(self._chip_id,0)]
            except KeyError:
                name = 'Unknown CHIP ID'
                
            log.info('Chip ID: {hexid} - {name}'.format(hexid=self._chip_id, name=name))
        except NotImplementedError as e:
            pass
        
    def _disconnect(self):
        pass
    
    def _wait_ack(self, cmd, seconds=30):
        i = 1
        while True:
            try:
                self._wait_for_ack(cmd, timeout=1.0)
                break
            except TimeoutError as e:
                log.info('Waiting... {}s'.format(i))
                if i >= seconds:
                    raise
                else:                    
                    i += 1
    
    @_check_support(CMD_GO)
    def _go(self, address):
        self._send_data(CMD_GO, struct.pack(">I", address))        
        self._wait_for_ack(CMD_GO)
        
    @_check_support(CMD_READOUT_PROTECT)
    def _lock(self):
        self._send_data(CMD_READOUT_PROTECT)
        self._wait_for_ack(CMD_READOUT_PROTECT)
        self._wait_ack(CMD_READOUT_PROTECT, UNPROTECT_MAX_TIMEOUT)
        
    @_check_support(CMD_READOUT_UNPROTECT)
    def _unlock(self):
        self._send_data(CMD_READOUT_UNPROTECT)
        self._wait_for_ack(CMD_READOUT_UNPROTECT)
        self._wait_ack(CMD_READOUT_UNPROTECT, MASSERASE_MAX_TIMEOUT)
        
    def _erase_page(self, p):
        self._send_data(CMD_ERASE, (p,))        
        self._wait_for_ack(CMD_ERASE)
        self._wait_ack(CMD_ERASE, MASSERASE_MAX_TIMEOUT)
                    
    @_check_support(CMD_ERASE)
    def _erase(self, pages):
        if len(pages) == 0:
            log.info('Mass erasing. Please wait..')
            self._erase_page(0xFF);
        else:
            for p in pages:
                log.info('Erasing sector {:02X}'.format(p))
                self._send_data(CMD_ERASE, (0,))        
                self._wait_for_ack(CMD_ERASE)
                self._erase_page(p);
                
    
    @_check_support(CMD_WRITE_MEMORY)  
    def _write(self, address, data):
        size = len(data)
        
        last_p = -1
        for i in range(0, size, 256):
            p = int(100.0 * i / size)
            if (last_p == -1) or (p - last_p >= 10):
                log.info('Progress: {}%'.format(p))
                last_p = p
            self._write_page(address+i, data[i:i+256])
        log.info('Progress: 100%')
    
    def _write_page(self, address, data):
        size = len(data)
        self._send_data(CMD_WRITE_MEMORY, struct.pack(">IB", address, size - 1))        
        self._wait_for_ack(CMD_WRITE_MEMORY)
        
        for i in range(0, size, 8):
            self._send_data(BYTE_DATA, data[i:i+8])      
            self._wait_for_ack(CMD_WRITE_MEMORY)
        
        self._wait_for_ack(CMD_WRITE_MEMORY)        
        
    @_check_support(CMD_READ_MEMORY)  
    def _read(self, address, size):

        total = size
        last_p = -1
        data = bytearray()
        while size > 0:
            p = int(100.0 * (total-size) / total)
            if (last_p == -1) or (p - last_p >= 10):
                log.info('Progress: {}%'.format(p))
                last_p = p
                
            to_read = min(256, size)
            
            page = self._read_page(address, to_read)
            data += page
            
            address += to_read
            size -= to_read
        
        log.info('Progress: 100%')
        
        return data
    
    def _read_page(self, address, size):
        self._send_data(CMD_READ_MEMORY, struct.pack(">IB", address, size - 1))        
        self._wait_for_ack(CMD_READ_MEMORY)
        
        page = bytearray()
        for _ in range(0, size, 8):
            data = self._recv_data(CMD_READ_MEMORY)
            page += data
        
        self._wait_for_ack(CMD_READ_MEMORY)
        
        return page

    def _speed(self, bps):
        if bps == 125000:
            code = 1
        elif bps == 250000:
            code = 2
        elif bps == 500000:
            code = 3
        elif bps == 1000000:
            code = 4
        else:
            raise NotImplementedError('Unsupported speed %d bps' % (bps,))

        self._send_data(CMD_CHANGE_SPEED, struct.pack(">B", code))
