#!/usr/bin/env python

''' Neural network test '''

import sys, random, math, array
from PIL import Image

from neulib.neuutil import *
from neulib.pgutil import *
import neulib.neulut as neulut
#neulut.VERBOSE = 2

from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Cipher import Salsa20
import secrets
import bluepy3

#print(dir(secrets))
#sys.exit()

if __name__ == '__main__':

    sumx = Image.new("L", (800,602), color=(0) )
    pp = Image.new("L", (800,300), color=(20) )
    #pp2 = Image.new("L", (800,300), color=(30) )

    rrr = bytearray()
    #for aa in range(300):
    #    for bb in range(800):
    #        rrr += bytearray((secrets.randbits(8),))
    for aa in range(300):
        rrr += Random.get_random_bytes(800)

    #for aa in range(300):
    #    rrr += b"a" * 800

    #key = b'0123456789012345'
    #key = b'0000000000000000'
    key = Random.get_random_bytes(16)

    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext =  cipher.encrypt(rrr)
    pp = Image.frombytes("L", (800, 300), ciphertext)

    #rrr = bytearray()
    #for aa in range(300):
    #    rrr += Random.get_random_bytes(800)
    #cipher = AES.new(key, AES.MODE_CBC)
    #cipher = Salsa20.new(key)
    #ciphertext2 =  cipher.encrypt(rrr)
    #ciphertext2 =  bluepy3.encrypt(rrr, "")
    ciphertext2 =  bluepy3.encrypt(rrr, key)
    pp2 = Image.frombytes("L", (800, 300), ciphertext2)

    #for aa in range(sumx.size[0]) :
    #    for bb in range(sumx.size[1]-1) :
    #        if bb < sumx.size[1] / 2:
    #            rrr = Random.get_random_bytes(3)
    #
    #            sumx.putpixel((aa, bb), rrr[2])
    #        else:
    #            rrr = secrets.randbits(8)
    #            sumx.putpixel((aa, bb + 1), rrr)

    sumx.paste(pp, (0, 0))
    sumx.paste(pp2, (0, 301))

    #print(dir())
    #secure_bits = secrets.randbits(8)
    #print(secure_bits)
    #sys.exit(0)
    sumx.show()

# EOF
