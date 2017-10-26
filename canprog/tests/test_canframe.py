'''
Created on 26.10.2017

@author: mborowicz
'''
import unittest

import canbus

class Test(unittest.TestCase):

    def testConstructor(self):
        with self.assertRaises(TypeError):
            canbus.CanFrame()
        
        with self.assertRaises(ValueError):
            canbus.CanFrame(mid=-1)
            
        with self.assertRaises(ValueError):
            canbus.CanFrame(mid=-1, extended=True)
        
        with self.assertRaises(ValueError):
            canbus.CanFrame(mid=0x800)
        
        with self.assertRaises(ValueError):
            canbus.CanFrame(mid=0x20000000, extended=True)
    
        f = canbus.CanFrame(mid=0, dlc=2, remote=True)
        self.assertEqual(f.mid, 0, 'wrong message id')
        self.assertEqual(f.dlc, 2, 'wrong dlc')
        self.assertEqual(f.is_remote, True, 'wrong remote type')
            


if __name__ == "__main__":
    unittest.main()