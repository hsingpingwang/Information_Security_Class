# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 00:33:47 2019

@author: chinya
"""

from Crypto.Util.number import long_to_bytes
import math, sys, Rsa_generate

global p,q,n,e,d,phi_n,ciphertext
e = 65537

# 中國餘式定理decrypt端(接收端)保留p,q不銷毀，用以加速解密
def chinese_remainder_theorem(ciphertext,p,q,e):
    # 確保p>q，在EEA(p,q)時才不會有Error
    if(p<q):
        temp = p
        p = q
        q = temp
    # 計算dp
    gcd, s, t = Rsa_generate.EEA((p-1), e)
    if gcd == (s*(p-1) + t*e):
        dp = t % (p-1)
    # 計算dq
    gcd, s, t = Rsa_generate.EEA((q-1), e)
    if gcd == (s*(q-1) + t*e):
        dq = t % (q-1)
    # 計算q^-1
    gcd, s, t = Rsa_generate.EEA(p, q)
    if gcd == (s*p + t*q):
        qInv = t % p
    # 用square and multiply 計算最後所得
    m1 = Rsa_generate.square_and_multiply(ciphertext, dp, p)
    m2 = Rsa_generate.square_and_multiply(ciphertext, dq, q)
    temp = Rsa_generate.square_and_multiply((m1-m2), 1, p)
    u =  Rsa_generate.square_and_multiply((qInv*temp), 1, p)
    x = m2+u*q
    return x

# 當被Rsa_encrypt.py 呼叫時，產生p,q,n,e,d,phi_n
# 並保留p,q,n,e,d在此decrypt端(接收端)，用以在解密時用中國餘式定理加速解密 
def generate(bits):
    #以bits大小來給定pq值
    global p,q,n,e,d,phi_n
    p = Rsa_generate.generate_primes(n=bits, k=1)[0]
    q = Rsa_generate.generate_primes(n=bits, k=1)[0]
    
    #計算n和phi_n
    n = p * q
    phi_n = (p - 1) * (q - 1)

    while True:
        e = 65537 #因為加速大數字加解密，公鑰e值約定為較小數字，所以bits數不能小於e
        if math.gcd(e, phi_n) == 1:
            #計算d: 利用擴展歐幾里得算法找e的反元素
            gcd, s, t = Rsa_generate.EEA(phi_n, e)
            if gcd == (s*phi_n + t*e):
                d = t % phi_n
                break
    return n

# 當被Rsa_encrypt.py 呼叫時，接收ciphertext
def receive(c):
    global ciphertext
    ciphertext = c
    # check ciphertext接收到
    if ciphertext == 0: 
        print("not received ciphertext\n")
    else:
        print("received ciphertext: ", ciphertext)
        if ciphertext > n:
            print("Error: n's bits are too small to decrypt ciphertext\n")
        else:
            # 因為保留n=p*q所以用chinese remainder theorem 加速解密出plaintext
            m = chinese_remainder_theorem(ciphertext,p,q,e)
            temp = str(long_to_bytes(m))
            l = len(temp)-1
            plaintext = temp[2:l]
            print("get plaintext: ",plaintext)
    
# 當指令直接呼叫Rsa_decrypt.py時執行main
def main():
    #從指令得指定的ciphertext, n, d
    cmd_list = sys.argv[1:]
    ciphertext = int(cmd_list[0])
    n = int(cmd_list[1])
    d = int(cmd_list[2])
    if n != 0 and d != 0:
        print("\nget privateKey(n,d): ", n, d)
        if ciphertext > n: 
            print("Error: n's bits are too small to decrypt ciphertext")
        else:
            # 因為此時只有privateKey(n,d)所以用square and multiply解密出plaintext
            # 而無法用chinese remainder theorem 加速
            m = Rsa_generate.square_and_multiply(ciphertext, d, n)
            temp = str(long_to_bytes(m))
            l = len(temp)-1
            plaintext = temp[2:l]
            print("get plaintext: ", plaintext)
    
if __name__ == '__main__':
    main()