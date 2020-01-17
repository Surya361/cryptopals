#!/bin/python
import base64
import itertools
from itertools import cycle

def score(s):
	freq = {}
	freq[' '] = 700000000
	freq['e'] = 390395169
	freq['t'] = 282039486
	freq['a'] = 248362256
	freq['o'] = 235661502
	freq['i'] = 214822972
	freq['n'] = 214319386
	freq['s'] = 196844692
	freq['h'] = 193607737
	freq['r'] = 184990759
	freq['d'] = 134044565
	freq['l'] = 125951672
	freq['u'] = 88219598
	freq['c'] = 79962026
	freq['m'] = 79502870
	freq['f'] = 72967175
	freq['w'] = 69069021
	freq['g'] = 61549736
	freq['y'] = 59010696
	freq['p'] = 55746578
	freq['b'] = 47673928
	freq['v'] = 30476191
	freq['k'] = 22969448
	freq['x'] = 5574077
	freq['j'] = 4507165
	freq['q'] = 3649838
	freq['z'] = 2456495
	score = 0
	for c in s.lower():
		if c in freq:
			score += freq[c]
	return score


def xor(txt,key,score=False):
	encoded = [chr(ord(x) ^ ord(y)) for (x,y) in zip(cycle(key), txt) ]
	total = 0
	if score:
		for i in encoded:
			if (127 > ord(i) and ord(i) > 0):
				total += 1
		return encoded,total
	return encoded

def frequency_analysis(hex):
	frequency_alphabet = {}
	for i in hex:
		frequency_alphabet[i] = frequency_alphabet.get(i,1) + 1
	return sorted(frequency_alphabet.iteritems(), key=lambda (k,v): (v,k), reverse=True)

def guess_key(string):
	max_score = None
	english_plaintext = None
	key = None

	for i in range(256):
		plaintext = ''.join(xor(string, chr(i)))
		pscore = score(plaintext)

		if pscore > max_score or not max_score:
			max_score = pscore
			english_plaintext = plaintext
			key = chr(i)
	return english_plaintext

def index_of_coincidence(text):
	n = len(''.join(e for e in text if e.isalnum()))
	sum = 0
	alpha = set(''.join(e for e in text if e.isalnum()))
	for char in alpha:
		c = text.count(char)
		sum = sum + (c * (c-1))
	return float(sum)/(n *(n-1))

def hamming_distance(x,y):
	list = [bin(ord(a) ^ ord(b)).count("1") for (a,b) in zip(x,y)]
	return sum(list)

def normalized_hamming_distance(string, len):
	min_hamming_distance = 0
	for i in range(2):
		#print string[i:len*(i+1)], string[len*(i+1):len*(i+2)]
		min_hamming_distance += (hamming_distance(string[i:len*(i+1)], string[len*(i+1):len*(i+2)]))/float(len)
		#print min_hamming_istance
	return min_hamming_distance/2.0

def get_blocks(text, le):
	blocks = []
	for i in range(le):
		j = i
		string = ""
		#print type(j), type(text)
		while j < len(text):
			string = string + text[j]
			j = j + le
		blocks.append(string)
	return blocks

def key_sizes(string):
	key_hamming = {}
	for i in range((len(string)/10)):
		key_hamming[i+1] = normalized_hamming_distance(string,i+1)
	sorted_dic = sorted(key_hamming.iteritems(), key=lambda (k,v): (v,k))
	return sorted_dic

def get_avg_ioc(text, key_size):
	ioc = []
	for block in get_blocks(text, key_size):
		#print block
		ioc.append(index_of_coincidence(block))
	return sum(ioc)/key_size

def key_sizes_ioc(string):
	key_ioc = {}
	for i in range(2,40):
		key_ioc[i+1] = get_avg_ioc(string,i+1)
	sorted_dic = sorted(key_ioc.iteritems(), key=lambda (k,v): (v,k), reverse=True)
	return sorted_dic

def rearrange(block_arr):
	array_length = len(block_arr)
	word_len = len(block_arr[0])
	final_array = ["0"] * (array_length * word_len)
	#print array_length * word_len
	for i in range(array_length):
		for j in range(len(block_arr[i])):
			#print (j*(array_length))+i
			final_array[(j*(array_length))+i] = block_arr[i][j]
	return ''.join(''.join(final_array).strip('0'))

def main():
	text = "hYX5lIZFmdDZjXCU0MG7Z4/K/JyeR5nK1Y04wM7NoC6K1/6Y0EPWyNKNNZKYy6Rnicz2nYRF3NPIkX2D3cqiMoWF+ZSGRZnN3YojhdyEoS6D17GFn0zQydnZPYXZyr8pg9exnZFW3J3QkD6H3dazI5zK/ZyERZnQ2Zg+idbDuiKNy/XVhEjWyNuRJMDawbAog8OxlNBN1t7XkD6HmNC3K5jKsYWcRdjO2dkxwNvLuzeN1/6AnkSZydSccIbR1rNnjsD4m5cA2tjOjTGJ1oSiL47Q5dWcSc/Y2NkniN3Ws2eNyf3Vk0jY09ucNMyYx74mjYXlkIJS0N/QnHCC3cWjM5jN8IHQV9bQ3Zd3k5jAtz6Fy7Gcl07Wz92XJMDfy7kjhMDj1Z5J3tXIinCJ1oS3NZnL5ZycANHYztkmj9HHs2ebzfCB0FbW1N+ccI3X1rNnm830m9BZ1sjSnnCB1sD2JZ/N9NWCT93YnI0/wNDFpDWYzfiG0E3Y05yRMYSYz7M3jcv11YJP3dicliWSmNO/KZjN+IbQT83V2YtwiNHX9i+bxOLVk0/U1NKecInW0LlnhMCxmJlH0cmckTGW3YShKJ/KsYaVTsrUyJAmhZjMvzSfyrGRkVLQ09vZMY7chKUwmM34htBPzdXZi3CN2cr2Do2F9YeFTtLY0tVwltnNuGqEwLGdkUSZ2dOXNcDVy6UzmMqxhp9N3J3LkT/A2dazZ5XA5dW5ANfI0Zs1kpjMvyqEwL3VhE/WkZyRMZOY1rM0hcuxgZhFmd7diiWB1IS1KITAvdWET9aRnJExk5jGsyKY1/Cbg0bWz9GcNMDN0KIijYXlkIJS0N/QnHCC3cWjMw=="
	text = text.decode("base64")
	length = len(text)
	keys = [(16,1.0)]
	assert rearrange(get_blocks("hello world",2)) == "hello world"
	print(keys)
	for key in keys:
		final = []
		for block in get_blocks(text,key[0]):
			final.append(guess_key(block))
		print(key)
		print(rearrange(final))

if __name__ == "__main__":
	main()
