#! /usr/bin/python3
from Crypto.Util.number import bytes_to_long, long_to_bytes
from random import randrange
import sys, math, random
cmd = sys.argv[1:]
#extended gcd
def eGCD(a,b):
	assert a>b
	x0, x1, y0, y1 = 1,0,0,1
	while a!= 0:
		q, b ,a = b//a, a, b%a
		x0,x1=x1,x0-q*x1
		y0,y1=y1,y0-q*y1
	return b,y0,x0

def square_and_multiply(a,b):
	#change exponential to binary
	exp = bin(b)
	value = a
	for i in range(3, len(exp)): #start with 0b
		value = value * value #square
		if(exp[i:i+1]=='1'):
			value = value * a #multiply
	return value

def miller_rabin_test(a,b):
	if a==2 or a==3:
		return True
	if a%2==0:
		return False
	r,s=0,a-1
	while s%2==0:
		r+=1
		s//=2
	for _ in range(b):
		x = random.randrange(2,a-1)
		y = pow(x,s,a)
		if y == 1 or y == a-1:
			continue
		for _ in range(r-1):
			y = pow(y,2,a)
			if y == a-1:
				break
		else:
			return False
	return True 	
def gen_prime(n=512,k=1):
	assert k>0
	assert n>0 and n<4096
	steps = math.floor(math.log(2**n)/2)
	x=random.getrandbits(n)
	prime=[]
	while k>0:
		if miller_rabin_test(x,10): #set test rounds
			prime.append(x)
			k=k-1
		x=x+1
	return prime
def initialStep():
	size=int(cmd[1])
	p=gen_prime(size,1)[0]
	q=gen_prime(size,1)[0]
	n=p*q
	phi = (p-1)*(q-1)
	while True:
		e=random.randrange(1,phi-1)
		if math.gcd(e,phi)==1:
			gcd, a, b = eGCD(phi,e)
			if gcd == (a*phi+b*e):
				d = b % phi #calculate inverse d
				break
	print('p=',p)
	print('q=',q)
	print('n=',n)
	print('e=',e)
	print('d=',d)
if(cmd[0]=='init'):
	initialStep()
#encryption step
if(cmd[0]=='-e'):
	plaintext = cmd[1]
	n = int(cmd[2])
	e = int(cmd[3])
	ciphertext = bytes_to_long(plaintext.encode('ascii'))
	if ciphertext > n:
		print("key is too small for this message")
	else:
		ciphertext = square_and_multiply(ciphertext,e)
		ciphertext = ciphertext % n
		print(ciphertext)
#decryption step
if(cmd[0]=='-d'):
	ciphertext = int(cmd[1])
	n = int(cmd[2])
	d = int(cmd[3])
	temp = square_and_multiply(ciphertext,d)
	temp = temp % n
	text = str(long_to_bytes(temp))
	output = text[2:len(text)-1]
	print(output)