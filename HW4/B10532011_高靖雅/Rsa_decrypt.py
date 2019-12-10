# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 00:33:47 2019

@author: small
"""

from Crypto.Util.number import long_to_bytes
import sys

def square_and_multiply(x, k, p=None):

    b = bin(k).lstrip('0b')
    r = 1
    for i in b:
        r = r**2
        if i == '1':
            r = r * x
        if p:
            r %= p
    return r


def main():
    cmd_list = sys.argv[1:]
    ciphertext = int(cmd_list[0])
    n = int(cmd_list[1])
    e = int(cmd_list[2])
    
    assert ciphertext < n
    m = square_and_multiply(ciphertext, e, n)
    plaintext = m

    print(plaintext)
    
if __name__ == '__main__':
    main()