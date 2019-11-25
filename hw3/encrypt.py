#! /usr/bin/python3
from PIL import Image, ImageFile
from Crypto import Random
from Crypto.Cipher import AES
import math, sys, binascii

cmd_list = sys.argv[1:]
key = cmd_list[1]
key = key[2:]
photo = cmd_list[2]
mode = cmd_list[0]

im=Image.open(photo)
im.save("input_encrypt.ppm")
f=open('input_encrypt.ppm','rb')

###image header info
fout=open('encrypt.ppm','wb')
for i in range (3):
	fout.write(f.readline())

block_size=16
total_bytes = im.width * im.height * 3
IV= Random.new().read(block_size)

if(mode == 'ECB'):
	encryption = AES.new(key.encode('utf8'),AES.MODE_ECB)
elif(mode == 'CBC'):
	encryption = AES.new(key.encode('utf8'),AES.MODE_CBC,IV)
elif(mode == 'CFB'):
	encryption = AES.new(key.encode('utf8'),AES.MODE_CFB,IV)
elif(mode == 'OFB'):
	IV = 16 * '\x00'
	encryption = AES.new(key.encode('utf8'),AES.MODE_OFB,IV.encode('utf8'))
else:
	print("not accepted mode")
	sys.exit()

plaintext=binascii.unhexlify(binascii.hexlify(f.read()))
padding = (block_size-len(plaintext)%block_size)
plaintext+=bytes([padding])*padding
turns = math.ceil(total_bytes / 16)
index=0
while(index<turns*16):
	one_block_text = plaintext[index:index+16]
	fout.write(encryption.encrypt(one_block_text))
	index=index+16	

ImageFile.LOAD_TRUNCATED_IMAGES = True
final=Image.open('encrypt.ppm')
final.save('encrypt.png','png')
final.show()
