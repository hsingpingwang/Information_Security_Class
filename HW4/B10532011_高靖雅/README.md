1、	分別測試 generate、encrypt、decrypt:
	Generate指令輸入:
		python Rsa_generate.py {bits數}
	 Output:
		p= XXXXXX
		q= XXXXXX
		n= XXXXXX
		e= XXXXXX
		d= XXXXXX

	Encrypt指令輸入:
		python Rsa_encrypt.py {plaintext} {n} {d}
	 Output:
		get publicKey(n,e): XXXXXX XXXXXX
		get ciphertext: XXXXXXXX

	Decrypt指令輸入:
		python Rsa_decrypt.py {ciphertext} {n} {e}
	 Output:
		get privateKey(n,d): XXXXXXX XXXXXX
		get plaintext:　XXXXXXXXX

2、 	測試完整加解密傳送流程:
	指令輸入:
		python Rsa_encrypt.py {bits數} {plaintext}
	Output:
		get publicKey(n,e): XXXXXX XXXXXX
		get ciphertext: XXXXXXXX
		
		received ciphertest: XXXXXXX
		get plaintext: XXXXXXXX
