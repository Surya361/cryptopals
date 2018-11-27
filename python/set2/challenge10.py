from Crypto.Cipher import AES
import base64

def get_data(file_name):
    fd = open(file_name,'r')
    cont = fd.read()
    content = cont.replace('\n','')
    return base64.b64decode(content)

def split(message, key_len):
    return [ message[i:i+key_len] for i in range(0, len(message), key_len)]

def xor(x,y):
    if type(x) is str and type(y) is str:
        return ''.join([ chr(ord(a) ^ ord(b)) for a,b in zip(x,y) ])
    elif type(y) is str:
        return ''.join([ chr(a ^ ord(b)) for a, b in zip(x, y)])
    elif type(x) is str:
        return ''.join([chr(ord(a) ^ b) for a, b in zip(x, y)])
    else:
        return ''.join([chr(a ^ b) for a, b in zip(x, y)])



def pkcs_7_padding(message, key_len):
    ar = split(message, key_len)
    ar[-1] += chr(key_len - len(ar[-1])) * (key_len- len(ar[-1]))
    return ar

def encrypt_cbc(message, IV, key):
    blocks = pkcs_7_padding(message, len(key))
    initialization_vector = IV
    cipher_text = []
    encoder_suite = AES.new(key, AES.MODE_ECB)
    for block in blocks:
        cipher = encoder_suite.encrypt(xor(block, initialization_vector))
       # print(type(cipher))
        cipher_text.append(cipher)
        initialization_vector = cipher
    return cipher_text[0]

def decrypt_cbc(message,IV,key):
    blocks = split(message, len(key))
    initialization_vector = IV
    plain_text = []
    decoder_suite = AES.new(key, AES.MODE_ECB)
    for block  in blocks:
        plain = xor(decoder_suite.decrypt(block), initialization_vector)
        plain_text.append(plain)
        initialization_vector = block
    return ''.join(plain_text)

iv = chr(0) * 16
print(decrypt_cbc(get_data("10.txt"),iv,"YELLOW SUBMARINE"))
print(decrypt_cbc(encrypt_cbc("this is a test", "aaaabbbbaaaabbbb", "bbbbccccddddeeee"), "aaaabbbbaaaabbbb",  "bbbbccccddddeeee"))