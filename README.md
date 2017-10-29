# canprog

## Main features
- Support STM32 CAN-BUS ROM bootloader
- Easily expand with other CAN-BUS protocols
- Support iHEX and binary format files
- Object oriented architecture
- Command-line interface
- Socket-CAN driver for CAN-BUS low level operations

## Todo
- [ ] Other microcontroller protocols
- [ ] Other CAN-BUS interfaces
- [ ] Autocalculating sectors for erasing (for STM32)
- [ ] Memory write protect/unprotect (form STM32)
- [ ] TDD tests

## Requirements
- Compatible PC CAN-BUS adapter 
- Linux + Python3
- Enabled SocketCAN driver
- Board with STM32 with CAN interface

### Driver instalation
```
modprobe can
modprobe can-raw
modprobe slcan
slcand -o -c -f -s4 /dev/ttyUSB0 slcan0
ip link set up slcan0
```

### App instalation
```
sudo pip install canprog
```

## Usage:
### General usage + configuration
```
usage: canprog [-h] [--verbose] [--version] [-n NAME] [-i {socketcan}]
               [-f {hex,bin}]
               {stm32} ...

Command-line tool to flashing devices by CAN-BUS.

others:
  -h, --help      show this help message and exit
  --verbose       enable verbose output
  --version       show program's version number and exit

configuration:
  -n NAME         interface name (default: slcan0)
  -i {socketcan}  interface type (default: socketcan)
  -f {hex,bin}    file format (default: hex)

protocols:
  {stm32}
    stm32         STM32 ROM bootloader
```
### STM32 bootloader options
```
usage: canprog stm32 [-h] {write,read,erase,go,lock,unlock} ...

others:
  -h, --help            show this help message and exit

commands:
  {write,read,erase,go,lock,unlock}
    write               write file to target memory
    read                read target memory to file
    erase               erase target memory
    go                  start program application
    lock                enable readout protection
    unlock              disable readout protection
```
### Usage examples:
```
canprog stm32 write image.hex
canprog -f bin stm32 write image.bin -a 0x08000000
canprog stm32 read dump.hex -s 0x200
canprog stm32 lock
canprog stm32 erase -P 0 1 2 3
```
### Example output:
```
[13:41:25.931] main INFO: Connecting target
[13:41:25.935] stm32 INFO: Bootloader initialized
[13:41:25.944] stm32 INFO: Bootloader version: 2.0
[13:41:25.947] stm32 INFO: Read protection: 0x0000
[13:41:25.950] stm32 INFO: Chip ID: 0x0413 - STM32F40xxx/41xxx
[13:41:25.950] main INFO: Connected
[13:41:25.958] main INFO: Writing memory at 0x08000000:6548
[13:41:25.958] stm32 INFO: Progress: 0%
[13:41:26.201] stm32 INFO: Progress: 11%
[13:41:26.429] stm32 INFO: Progress: 23%
[13:41:26.657] stm32 INFO: Progress: 35%
[13:41:26.895] stm32 INFO: Progress: 46%
[13:41:27.136] stm32 INFO: Progress: 58%
[13:41:27.371] stm32 INFO: Progress: 70%
[13:41:27.617] stm32 INFO: Progress: 82%
[13:41:27.908] stm32 INFO: Progress: 93%
[13:41:28.065] stm32 INFO: Progress: 100%
[13:41:28.065] main INFO: Successful
[13:41:28.065] main INFO: Writing memory at 0x08004000:16
[13:41:28.065] stm32 INFO: Progress: 0%
[13:41:28.074] stm32 INFO: Progress: 100%
[13:41:28.074] main INFO: Successful
[13:41:28.074] main INFO: Disconnecting target
[13:41:28.074] main INFO: Disconnected
```

