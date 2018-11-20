import base64
from itertools import cycle

def xor(txt,key):
	encoded = [chr(ord(x) ^ ord(y)) for (x,y) in zip(cycle(key), txt) ]
	score = 0
	for i in encoded:
		if (127 > ord(i) and ord(i) > 30) or ord(i) in [9,10]:
			score += 1
	return encoded,score


def frequency_analysis(hex):
	frequency_alphabet = {}
	for i in hex:
		frequency_alphabet[i] = frequency_alphabet.get(i,1) + 1
	return frequency_alphabet

def char_fequency(string):
	sorted_dic = sorted(frequency_analysis(string).iteritems(), key = lambda (k,v): (v,k.lower()), reverse=True)
	#print sorted_dic
	if sorted_dic[0][0] not in ['e', 't', 'a', 'o', 'i',' ']:
		return False
	return True


def index_of_coincidence(text):
	n = len(''.join(e for e in text if e.isalnum()))
	sum = 0
	alpha = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
	for char in alpha:
		c = text.count(char)
		sum = sum + (c * (c-1))
	return float(sum)/(n *(n-1))

possible_array = []
def guess_key(sorted_dic,string):
	for i in sorted_dic:
		key,score = xor(i[0], 'a')
		#print len(string)
		plain, score = xor(string, key)
		if score < len(string):
			continue
		else:
			plain_txt = ''.join(plain)
			possible_array.append((plain_txt, index_of_coincidence(plain_txt)))


def main():
	file = open('4.xtx','r')
	for string in file:

		string = string.strip()
		#string = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
		#print string
		string = string.decode('hex')
		string_dic =  frequency_analysis(string)
		sorted_dic = sorted(string_dic.iteritems(), key=lambda (k,v): (v,k), reverse=True)
		guess_key(sorted_dic,string)
		#break
	print sorted(possible_array, key=lambda value: value[1], reverse=True)

if __name__ == "__main__":
	main()