import base64
from itertools import cycle

def xor(txt,key,score=False):
	encoded = [chr(ord(x) ^ ord(y)) for (x,y) in zip(cycle(key), txt) ]
	score = 0
	if score:
		for i in encoded:
			if (127 > ord(i) and ord(i) > 30) or ord(i) in [9,10]:
				score += 1
		return encoded,score
	return encoded

def main():
	print ''.join(xor('Burning \'em, if you ain\'t quick and nimble\nI go crazy when I hear a cymbal','ICE')).encode('hex')

if __name__ == "__main__":
	main()