# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 00:12:09 2019

@author: small
"""
from Crypto.Util.number import bytes_to_long
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
    # m = int(cmd_list[0])
    plaintext = str(cmd_list[0])
    n = int(cmd_list[1])
    d = int(cmd_list[2])

    m = bytes_to_long(plaintext.encode('ascii'))
    if m > n: 
        print("Error: n is too small to encrypt plaintext")
    else:
        ciphertext = square_and_multiply(m, d, n)
        print(ciphertext)
    
if __name__ == '__main__':
    main()