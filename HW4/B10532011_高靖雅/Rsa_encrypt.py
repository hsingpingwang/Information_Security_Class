# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 00:12:09 2019

@author: chinya
"""
from Crypto.Util.number import bytes_to_long
import sys, Rsa_decrypt, Rsa_generate

def main():
    cmd_list = sys.argv[1:]
    
    # 當指令呼叫Rsa_encrypt.py {bits數}{plaintext}時 
    # 呼叫Rsa_decrypt.py來產生publicKey所需的n
    # 並使得decrypt端(接收端)保留n=p*q以及privateKey所需的d
    if len(cmd_list)==2:
        bits = int(cmd_list[0])
        plaintext = str(cmd_list[1])
        n = Rsa_decrypt.generate(bits) 
        e=65537
    else: 
        # 當指令直接呼叫Rsa_encrypt.py{plaintext}{n}{e}時
        # 從指令得指定的plaintext, n, e
        plaintext = str(cmd_list[0])
        n = int(cmd_list[1])
        e = int(cmd_list[2])
    # check publicKey(n,e)
    # 並用square and multiply計算ciphertext
    if n != 0 and e != 0:
        print("\nget publicKey(n,e): ", n, e)
        m = bytes_to_long(plaintext.encode('ascii'))
        if m > n: 
            print("Error: n's bits are too small to encrypt plaintext\n")
        else:
            ciphertext = Rsa_generate.square_and_multiply(m, e, n)
            print("get ciphertext: ", ciphertext)
        
        # 當指令呼叫Rsa_encrypt.py {bits數}{plaintext}時 
        # 呼叫Rsa_decrypt.py來接收ciphertext    
        if len(cmd_list)==2:
            print()
            Rsa_decrypt.receive(ciphertext)
    else:
        print("not get the publicKey\n")
            
    
if __name__ == '__main__':
    main()