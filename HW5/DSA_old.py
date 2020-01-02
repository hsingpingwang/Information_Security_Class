# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 08:48:01 2020

@author: small
"""
import sys
from random import randrange
from hashlib import sha1
from gmpy2 import xmpz, to_binary, invert, powmod, is_prime


def generate_p_q(L, N):
    g = N  # g >= 160
    n = (L - 1) // g
    b = (L - 1) % g
    while True:
        # generate q
        while True:
            s = xmpz(randrange(1, 2 ** (g)))
            a = sha1(to_binary(s)).hexdigest()
            zz = xmpz((s + 1) % (2 ** g))
            z = sha1(to_binary(zz)).hexdigest()
            U = int(a, 16) ^ int(z, 16)
            mask = 2 ** (N - 1) + 1
            q = U | mask
            if is_prime(q, 20):
                break
        # generate p
        i = 0  # counter
        j = 2  # offset
        while i < 4096:
            V = []
            for k in range(n + 1):
                arg = xmpz((s + j + k) % (2 ** g))
                zzv = sha1(to_binary(arg)).hexdigest()
                V.append(int(zzv, 16))
            W = 0
            for qq in range(0, n):
                W += V[qq] * 2 ** (160 * qq)
            W += (V[n] % 2 ** b) * 2 ** (160 * n)
            X = W + 2 ** (L - 1)
            c = X % (2 * q)
            p = X - c + 1  # p = X - (c - 1)
            if p >= 2 ** (L - 1):
                if is_prime(p, 10):
                    return p, q
            i += 1
            j += n + 1


def generate_g(p, q):
    while True:
        h = randrange(2, p - 1)
        exp = xmpz((p - 1) // q)
        g = powmod(h, exp, p)
        if g > 1:
            break
    return g


def generate_keys(g, p, q):
    x = randrange(2, q)  # x < q
    y = powmod(g, x, p)
    return x, y


def generate_params(L, N):
    p, q = generate_p_q(L, N)
    g = generate_g(p, q)
    return p, q, g


def sign(M, p, q, g, x):
    if not validate_params(p, q, g):
        raise Exception("Invalid params")
    while True:
        k = randrange(2, q)  # k < q
        r = powmod(g, k, p) % q
        m = int(sha1(M).hexdigest(), 16)
        try:
            s = (invert(k, q) * (m + x * r)) % q
            return r, s
        except ZeroDivisionError:
            pass


def verify(M, r, s, p, q, g, y):
    if not validate_params(p, q, g):
        raise Exception("Invalid params")
    if not validate_sign(r, s, q):
        return False
    try:
        w = invert(s, q)
    except ZeroDivisionError:
        return False
    m = int(sha1(M).hexdigest(), 16)
    u1 = (m * w) % q
    u2 = (r * w) % q
    # v = ((g ** u1 * y ** u2) % p) % q
    v = (powmod(g, u1, p) * powmod(y, u2, p)) % p % q
    if v == r:
        return True
    return False


def validate_params(p, q, g):
    if is_prime(p) and is_prime(q):
        return True
    if powmod(g, q, p) == 1 and g > 1 and (p - 1) % q:
        return True
    return False


def validate_sign(r, s, q):
    if r < 0 and r > q:
        return False
    if s < 0 and s > q:
        return False
    return True


if __name__ == "__main__":
    N = 160
    L = 1024
    text = "MISIS rocks"    
    M = str.encode(text, "ascii")
    
    cmd_list = sys.argv[1:]
    mode = cmd_list[0]
    
    if(mode == "-keygen"):
        N = int(cmd_list[1])
        p, q, g = generate_params(L, N)
        x, y = generate_keys(g, p, q)
        
        data=open("PrivKey.txt",'w+')
        print( x, file=data)
        data.close()
        
        data=open('PubKey.txt','w+')
        print( p, file=data)
        print( q, file=data)
        print( g, file=data)
        print( y, file=data)
        data.close()
    elif(mode == "-sign"):
        text = cmd_list[1]
        M = str.encode(text, "ascii")
        
        with open('PubKey.txt') as f:
            pubkey = list(f)
        p = int(pubkey[0])
        q = int(pubkey[1])
        g = int(pubkey[2])
       # print(p,q,g, sep="\n")
        f.close()
        
        f = open('PrivKey.txt', 'r')
        x = int(f.read())
        f.close()
        
        r, s = sign(M, p, q, g, x)
        
        data=open("Sign.txt",'w+')
        print(r, file=data)
        print(s, file=data)
        data.close()
    elif(mode == "-verify"):
        r = cmd_list[1]
        s = cmd_list[2]
        
        with open('PubKey.txt') as f:
            pubkey = list(f)
        p = int(pubkey[0])
        q = int(pubkey[1])
        g = int(pubkey[2])
        y = int(pubkey[3])
        f.close()
        
        if verify(M, r, s, p, q, g, y):
            print('valid')
        else:
            print('invalid')