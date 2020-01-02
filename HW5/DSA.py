from fractions import gcd
import random
import sys
import hashlib
import math

# Primality Testing with the Rabin-Miller Algorithm
def rabinMiller(num):
    # Returns True if num is a prime number.

    s = num - 1
    t = 0
    while s % 2 == 0:
        # keep halving s while it is even (and use t
        # to count how many times we halve s)
        s = s // 2
        t += 1

    for trials in range(5): # try to falsify num's primality 5 times
        a = random.randrange(2, num - 1)
        v = pow(a, s, num)
        if v != 1: # this test does not apply if v is 1.
            i = 0
            while v != (num - 1):
                if i == t - 1:
                    return False
                else:
                    i = i + 1
                    v = (v ** 2) % num
    return True

def isPrime(num):

    if (num < 2):
        return False # 0, 1, and negative numbers are not prime


    lowPrimes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]

    if num in lowPrimes:
        return True

    # See if any of the low prime numbers can divide num
    for prime in lowPrimes:
        if (num % prime == 0):
            return False

    # If all else fails, call rabinMiller() to determine if num is a prime.
    return rabinMiller(num)


def generateLargePrime(keysize):
    # Return a random prime number of keysize bits in size.
    while True:
        num = random.randrange(2**(keysize-1), 2**(keysize))
        if isPrime(num):
            return num

def loopIsPrime(number):
	#looping to reduce probability of rabin miller false +
	isNumberPrime = True
	for i in range(0,20):
		isNumberPrime*=isPrime(number)
		if(isNumberPrime == False):
			return isNumberPrime
	return isNumberPrime	
def modexp( base, exp, modulus ):
        return pow(base, exp, modulus)
def squareAndMultiply(x,c,n):
	z=1
	#getting value of l by converting c into binary representation and getting its length
	c="{0:b}".format(c)[::-1] #reversing the binary string
	
	l=len(c)
	for i in range(l-1,-1,-1):
		z=pow(z,2)
		z=z%n
		if(c[i] == '1'):
			z=(z*x)%n
	return z

#function to compute inverse
def computeInverse (in1,in2):
    aL = [in1]
    bL = [in2]
    tL = [0]
    t = 1
    sL = [1]
    s = 0
    q = math.floor((aL[0]/bL[0]))
    r = (aL[0] - (q*bL[0]))

    while r > 0 :
        temp = (tL[0] - (q*bL[0]))
        tL[0] = t
        t = temp
        temp = (sL[0] - (q*s))
        sL[0] = s
        s = temp
        aL[0] = bL[0]
        bL[0] = r
        q = math.floor(aL[0]/bL[0])
        r = (aL[0] - (q*bL[0]))

    r = bL[0]

    inverse = s % in2
    return inverse

def shaHash(fileName):
	BLOCKSIZE = 65536
	hasher = hashlib.sha1()
	with open(fileName, 'rb') as afile:
		buf = afile.read(BLOCKSIZE)
		while len(buf) > 0:
			hasher.update(buf)
			buf = afile.read(BLOCKSIZE)
	#print(hasher.hexdigest())
	hex = "0x"+hasher.hexdigest()
	#print(int(hex,0))
	return int(hex,0) #returns int value of hash

def verification():
	if(len(sys.argv) < 3):
		print("Format: python sign.py filename")
	elif(len(sys.argv) == 3):	
		print("Checking the signature...")
		fileName = sys.argv[2]
		
		file1 = open("pubKey.txt","r")
		file2 = open("signature.txt","r")
		p=int(file1.readline().rstrip())
		q=int(file1.readline().rstrip())
		g=int(file1.readline().rstrip())
		h=int(file1.readline().rstrip())
		
		c1=int(file2.readline().rstrip())
		c2=int(file2.readline().rstrip())
		#print(c1)
		#print(c2)
		
		t1=shaHash(fileName)
		#print(t1)
		inverseC2 = computeInverse(c2,q)
		t1 = (t1*inverseC2)%q
		
		t2 = computeInverse(c2,q)
		t2 = (t2*c1)%q
		
		valid1 = squareAndMultiply(g,t1,p)
		valid2 = squareAndMultiply(h,t2,p)
		valid = ((valid1*valid2)%p)%q
		#print(valid)
		if(valid == c1):
			print("Valid signature")
		else:
			print("Invalid signature")

def sign():
	if(len(sys.argv) < 3):
		print("Format: python sign.py filename")
	elif(len(sys.argv) == 3):	
		print("Signing the file...")
		fileName = sys.argv[2]
		
		file1 = open("pubKey.txt","r")
		file2 = open("privKey.txt","r")
		p=int(file1.readline().rstrip())
		q=int(file1.readline().rstrip())
		g=int(file1.readline().rstrip())
		h=int(file1.readline().rstrip())
		a=int(file2.readline().rstrip())
		
		loop = True
		while loop:
			r = random.randint(1,q-1)
			c1 = squareAndMultiply(g,r,p)
			c1 = c1%q
			c2 = shaHash(fileName) + (a*c1)
			Rinverse = computeInverse(r,q)
			c2 = (c2*Rinverse)%q
			
			if(c1 != 0 and c2 != 0):
				loop = False
		
		#print(shaHash(fileName))	
		#print(c1)	
		#print(c2)	
		file = open("signature.txt","w")
		file.write(str(c1))
		file.write("\n")
		file.write(str(c2))
		print("cipher stored at signature.txt")	

def keyGeneration():
	
	print("Computing key values, please wait...")
	loop = True
	while loop:
		k=random.randrange(2**(415), 2**(416)) #416 bits
		q=generateLargePrime(160)
		p=(k*q)+1
		while not (isPrime(p)):
			k=random.randrange(2**(415), 2**(416)) #416 bits
			q=generateLargePrime(160)
			p=(k*q)+1
		L = p.bit_length()
		"""
		g=t^(p-1)/q  %  p
		if(g^q  % p = 1) we found g
		"""

		t = random.randint(1,p-1)
		g = squareAndMultiply(t, (p-1)//q, p)
		
		if(L>=512 and L<=1024 and L%64 == 0 and (math.gcd(p-1,q)) > 1 and squareAndMultiply(g,q,p) == 1):
		#if(L>=512 and L<=1024 and L%64 == 0):
			loop = False
			#print((p-1)%q)
			
			a = random.randint(2,q-1)
			h = squareAndMultiply(g,a,p)
			#print("p = ",p)
			#print("q = ",q)
			#print("g = ",g)
			#print("h = ",h)
			#print("a = ",a)
			
			file1 = open("pubKey.txt","w")
			file1.write(str(p))
			file1.write("\n")
			file1.write(str(q))
			file1.write("\n")
			file1.write(str(g))
			file1.write("\n")
			file1.write(str(h))
			file1.close()
			file2 = open("privKey.txt","w")
			file2.write(str(a))
			file2.close()
			
			print("Verification key stored at pubKey.txt and secret key stored at privKey.txt")

if __name__ == "__main__":    
    cmd_list = sys.argv[1:]
    mode = cmd_list[0]
    
    if(mode == "-keygen"):
        keyGeneration()
    elif(mode == "-sign"):
        sign()
    elif(mode == "-verify"):
        verification()