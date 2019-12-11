# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 23:19:51 2019

@author: chinya
"""
import random, math, sys

"""
參數: 正整數x 整數指數k optional modulus p
計算: x^k 或是 x^k mod p (p存在時)
"""
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

def miller_rabin_primality_test(p, s=5):
    # 2 是唯一的偶數且質數
    if p == 2: 
        return True
    # 若n是除了2外的偶數，則非質數
    if not (p & 1): 
        return False
    
    # p-1 = 2^u * r
    p1 = p - 1
    u = 0
    r = p1  

    while r % 2 == 0:
        r >>= 1
        u += 1

    # 若此時 p-1 = 2^u * r  holds
    assert p-1 == 2**u * r

    def witness(a):
        # True, 表此時有witness證明p不是質數
        # False, 表此時p可能是質數
        
        #用square and multiply 加速計算
        z = square_and_multiply(a, r, p)
        if z == 1:
            return False

        for i in range(u):
            z = square_and_multiply(a, 2**i * r, p)
            if z == p1:
                return False
        return True

    for j in range(s):
        a = random.randrange(2, p-2)
        if witness(a):
            return False

    return True

"""
以bitlength n來產生質數，直到產生k個質數後結束
質數測試的數字從隨機開始，測試是用整數
"""
def generate_primes(n=512, k=1):
    assert k > 0
    assert n > 0 and n < 4096

    # follows from the prime number theorem
    necessary_steps = math.floor( math.log(2**n) / 2 )
    # get n random bits as our first number to test for primality
    x = random.getrandbits(n)

    primes = []

    while k>0:
        #呼叫miller rabin test 來測試是否為質數
        if miller_rabin_primality_test(x, s=7):
            primes.append(x)
            k = k-1
        x = x+1

    return primes

"""
擴展歐幾里得演算法Extended Euclidean Algorithm(EEA)
參數: 正整數a,b 且 a > b
計算: gcd(a,b) = s*a + t*b
Return: ( gcd(a,b), s, t )

參考: https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm
"""
def EEA(a, b):
    
    assert a > b, 'a must be larger than b'
    x0, x1, y0, y1 = 1, 0, 0, 1
    while a != 0:
        q, b, a = b // a, a, b % a
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return  b, y0, x0

# 當指令直接呼叫Rsa_generate.py時執行main
def main():
    #從指令得指定的bits大小
    cmd_list = sys.argv[1:]
    bits = int(cmd_list[0])
    
    #以bits大小來給定pq值   
    p = generate_primes(n=bits, k=1)[0]
    q = generate_primes(n=bits, k=1)[0]
    
    #計算n和phi_n
    n = p * q
    phi_n = (p - 1) * (q - 1)
    
    #隨機找e且與phi_n-1互值並計算d
    while True:
        e = random.randrange(1, phi_n-1)
        if math.gcd(e, phi_n) == 1:
            #計算d: 利用擴展歐幾里得算法找e的反元素
            gcd, s, t = EEA(phi_n, e)
            if gcd == (s*phi_n + t*e):
                d = t % phi_n
                break
    
    print('\np= ',p)
    print('\nq= ',q)
    print('\nn= ',n)
    print('\ne= ',e)
    print('\nd= ',d)
 
if __name__ == '__main__':
    main()