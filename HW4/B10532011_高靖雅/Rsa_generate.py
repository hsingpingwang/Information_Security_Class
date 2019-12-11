# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 23:19:51 2019

@author: chinya

Generate prime numbers with the Miller-Rabin Primality Test.
"""
import random, math, sys

def square_and_multiply(x, k, p=None):
    """
    Square and Multiply Algorithm
    Parameters: positive integer x and integer exponent k,
                optional modulus p
    Returns: x**k or x**k mod p when p is given
    """
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
    if p == 2: # 2 is the only prime that is even
        return True
    if not (p & 1): # n is a even number and can't be prime
        return False

    p1 = p - 1
    u = 0
    r = p1  # p-1 = 2**u * r

    while r % 2 == 0:
        r >>= 1
        u += 1

    # at this stage p-1 = 2**u * r  holds
    assert p-1 == 2**u * r

    def witness(a):
        """
        Returns: True, if there is a witness that p is not prime.
                False, when p might be prime
        """
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

def generate_primes(n=512, k=1):
    """
    Generates prime numbers with bitlength n.
    Stops after the generation of k prime numbers.
    Caution: The numbers tested for primality start at
    a random place, but the tests are drawn with the integers
    following from the random start.
    """
    assert k > 0
    assert n > 0 and n < 4096

    # follows from the prime number theorem
    necessary_steps = math.floor( math.log(2**n) / 2 )
    # get n random bits as our first number to test for primality
    x = random.getrandbits(n)

    primes = []

    while k>0:
        if miller_rabin_primality_test(x, s=7):
            primes.append(x)
            k = k-1
        x = x+1

    return primes

def EEA(a, b):
    """
    Source: https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm
    Extended Euclidean Algorithm (EEA)
    Parameters: Positive integers a and b whereby a > b
    Returns: ( gcd(a,b), s, t )  such that gcd(a,b) = s*a + t*b
    """
    assert a > b, 'a must be larger than b'
    x0, x1, y0, y1 = 1, 0, 0, 1
    while a != 0:
        q, b, a = b // a, a, b % a
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return  b, y0, x0

def main():
    cmd_list = sys.argv[1:]
    bits = int(cmd_list[0])
    
    p = generate_primes(n=bits, k=1)[0]
    q = generate_primes(n=bits, k=1)[0]
    
    n = p * q
    
    phi_n = (p - 1) * (q - 1)

    while True:
        e = random.randrange(1, phi_n-1)
        if math.gcd(e, phi_n) == 1:

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