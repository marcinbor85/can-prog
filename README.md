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

## Usage:
`
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
`
`    
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
`