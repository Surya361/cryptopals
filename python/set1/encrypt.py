import base64
from itertools import cycle
from random import randint

FLAG="flag{this_is_a_dummy_flag}"
KEY_LEN=randint(1,40)

def encrypt(text,key):
	cipher = ''.join([chr(ord(x) ^ ord(y)) for (x,y) in zip(cycle(key), text) ])
	return cipher

def decrypt(cipher,key):
	plain = ''.join([chr(ord(x) ^ ord(y)) for (x,y) in zip(cycle(key), cipher) ])
	return plain


def main():
	key = __import__('os').urandom(KEY_LEN)
	text = FLAG + open('english.txt', 'r').read(200)
	cipher = encrypt(text,key)
	print base64.b64encode(cipher)
	plain = decrypt(cipher,key)
	print plain

if __name__ == "__main__":
	main()
