def hammingdistance(str1,str2):
    distance = 0
    ascii_str1 = [ord(i) for i in list(str1)]
    ascii_str2 = [ord(i) for i in list(str2)]
    for i,j in zip(ascii_str2,ascii_str1):
        c = i ^ j
        distance += list("{0:b}".format(c)).count("1")
    return distance




def distance(num1,num2):
	c = num2 ^ num1
	bytestring = list("{0:b}".format(10))
