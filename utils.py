from Crypto.PublicKey import RSA

key_pair = RSA.generate(1024)

public_key = key_pair.publickey().exportKey()
private_key = key_pair.exportKey()

print(public_key)
print(private_key)
