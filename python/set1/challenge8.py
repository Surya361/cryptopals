import codecs

def hamming_distance(x,y):
    list = [bin(a ^ b).count("1") for (a,b) in zip(x,y)]
    return sum(list)

def read_file(file_name):
    fd = open("8.txt","r")
    hammin_dis = []
    for line in fd:
        #hammin_dis.append(sum_hamming_distance(bytes(codecs.decode(line.strip(),"hex")),16))
        hammin_dis.append(dist_blocks(line.strip()))
    print(hammin_dis.index(min(hammin_dis)))

def split(array, n):
    return [array[i:i+n] for i in range(0, len(array), n)]

def dist_blocks(line):
    array = split(line, 16)
    return len(set(array))

def sum_hamming_distance(string,key_len):
    i = 0
    sum_hamming_distance = 0
    while i < len(string)-key_len-1:
        sum_hamming_distance += hamming_distance(string[0:key_len],string[i:i+key_len])
        i += key_len
    return sum_hamming_distance

read_file("test")