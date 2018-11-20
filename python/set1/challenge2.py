from itertools import cycle

def xor(txt,key):
	encoded = [chr(ord(x) ^ ord(y)) for (x,y) in zip(cycle(key), txt) ]
	return ''.join(encoded).encode('hex')
if __name__ == "__main__":
	print xor('1c0111001f010100061a024b53535009181c'.decode('hex'),'686974207468652062756c6c277320657965'.decode('hex'))