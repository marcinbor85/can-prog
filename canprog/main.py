'''
Created on 23.10.2017

@author: mborowicz
'''

import canbus

def run():
    f = canbus.CanFrame(mid=10, data=bytes([1,2,3]), dlc=1, remote=False, extended=False)
    print(f.is_extended)
    print(f)
    print(f.data[0])

if __name__ == '__main__':
    run()