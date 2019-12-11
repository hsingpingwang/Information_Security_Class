# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 00:12:09 2019

@author: chinya
"""
from Crypto.Util.number import bytes_to_long
import sys, Rsa_decrypt, Rsa_generate

def main():
    cmd_list = sys.argv[1:]
    if len(cmd_list)==2:
        bits = int(cmd_list[0])
        plaintext = str(cmd_list[1])
        n, e= Rsa_decrypt.generate(bits)
    else:
        plaintext = str(cmd_list[0])
        n = int(cmd_list[1])
        e = int(cmd_list[2])
        
    if n != 0 and e != 0:
        print("\nget publicKey(n,e): ", n, e)
        m = bytes_to_long(plaintext.encode('ascii'))
        if m > n: 
            print("Error: n's bits are too small to encrypt plaintext\n")
        else:
            ciphertext = Rsa_generate.square_and_multiply(m, e, n)
            print("get ciphertext: ", ciphertext)
        if len(cmd_list)==2:
            print()
            Rsa_decrypt.receive(ciphertext)
    else:
        print("not get the publicKey\n")
            
    
if __name__ == '__main__':
    main()