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
		python Rsa_encrypt.py {plaintext} {n} {e}
	 Output:
		get publicKey(n,e): XXXXXX XXXXXX
		get ciphertext: XXXXXXXX

	Decrypt指令輸入:
		python Rsa_decrypt.py {ciphertext} {n} {d}
	 Output:
		get privateKey(n,d): XXXXXXX XXXXXX
		get plaintext:　XXXXXXXXX

2、 	測試完整加解密傳送流程:

	注意: 因為測試完整流程是為大數字所設計，為了加速計算且避免1024bits的參數輸入上的麻煩，
		  所以公鑰e約定預設為65537，而指令輸入時bits數不能小於e
	
	指令輸入:
		python Rsa_encrypt.py {bits數} {plaintext}
	Output:
		get publicKey(n,e): XXXXXX XXXXXX
		get ciphertext: XXXXXXXX
		
		received ciphertext: XXXXXXX
		get plaintext: XXXXXXXX
