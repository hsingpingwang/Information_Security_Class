# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 00:33:47 2019

@author: chinya
"""

from Crypto.Util.number import long_to_bytes
import random, math, sys, Rsa_generate

global p,q,n,e,d,phi_n,ciphertext

def chinese_remainder_theorem(ciphertext,p,q,e):
    if(p<q):
        temp = p
        p = q
        q = temp
    gcd, s, t = Rsa_generate.EEA((p-1), e)
    if gcd == (s*(p-1) + t*e):
        dp = t % (p-1)
    gcd, s, t = Rsa_generate.EEA((q-1), e)
    if gcd == (s*(q-1) + t*e):
        dq = t % (q-1)
    gcd, s, t = Rsa_generate.EEA(p, q)
    if gcd == (s*p + t*q):
        qInv = t % p
    m1 = Rsa_generate.square_and_multiply(ciphertext, dp, p)
    m2 = Rsa_generate.square_and_multiply(ciphertext, dq, q)
    temp = Rsa_generate.square_and_multiply((m1-m2), 1, p)
    u =  Rsa_generate.square_and_multiply((qInv*temp), 1, p)
    x = m2+u*q
    return x

def generate(bits):
    global p,q,n,e,d,phi_n
    p = Rsa_generate.generate_primes(n=bits, k=1)[0]
    q = Rsa_generate.generate_primes(n=bits, k=1)[0]

    n = p * q
    
    phi_n = (p - 1) * (q - 1)

    while True:
        e = random.randrange(1, phi_n-1)
        while p-e<=1 or q-e<=1:
            e = random.randrange(1, phi_n-1)
        if math.gcd(e, phi_n) == 1:

            gcd, s, t = Rsa_generate.EEA(phi_n, e)
            if gcd == (s*phi_n + t*e):
                d = t % phi_n
                break
    return n, e

def receive(c):
    global ciphertext
    ciphertext = c
    if ciphertext == 0: 
        print("not received ciphertext\n")
    else:
        print("received ciphertext: ", ciphertext)
        if ciphertext > n:
            print("Error: n's bits are too small to decrypt ciphertext\n")
        else:
            m = chinese_remainder_theorem(ciphertext,p,q,e)
            temp = str(long_to_bytes(m))
            l = len(temp)-1
            plaintext = temp[2:l]
            print("get plaintext: ",plaintext)
    

def main():
    cmd_list = sys.argv[1:]
    ciphertext = int(cmd_list[0])
    n = int(cmd_list[1])
    d = int(cmd_list[2])
    if n != 0 and d != 0:
        print("\nget privateKey(n,d): ", n, d)
        if ciphertext > n: 
            print("Error: n's bits are too small to decrypt ciphertext")
        else:
            m = Rsa_generate.square_and_multiply(ciphertext, d, n)
            temp = str(long_to_bytes(m))
            l = len(temp)-1
            plaintext = temp[2:l]
            print("get plaintext: ", plaintext)
    
if __name__ == '__main__':
    main()