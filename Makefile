target: Encrypt Decrypt
	@g++     Encrypt.cpp   -o Encrypt
	@g++     Decrypt.cpp   -o Decrypt
clean:
	@rm Encrypt
	@rm Decrypt
