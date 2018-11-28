#!/bin/python3
from Crypto.Cipher import AES
import random

UID = 1

def parse_cookie(cookie):
    k_v = dict()
    for kv in cookie.split('&'):
        key, value = kv.split("=")
        k_v[key] = value

    return k_v

def split(message, key_len):
    return [ message[i:i+key_len] for i in range(0, len(message), key_len)]

def pkcs_7_padding(message, key_len):
    ar = split(message, key_len)
    ar[-1] += bytes([key_len - len(ar[-1])]) * (key_len - len(ar[-1]))
    return ar


def encryption_oracle(message, key):
    mesg = b"".join(pkcs_7_padding( message.encode(), len(key)))
    encryption_suite = AES.new(key, AES.MODE_ECB)
    cipher = encryption_suite.encrypt(mesg)
    return cipher

def sanity_clean(text):
    text = text.replace("&",'')
    text = text.replace("=",'')
    return text

def encode(cookie_dic):
    encoded_cookie = ""
    for k,v in cookie_dic.items():
        encoded_cookie += "&"+ str(k) +"=" + str(v)
    return encoded_cookie[1:]

def remove_padding(plain, key_len):
    if type(plain[-1]) is int and plain[-1] < key_len:
        pad_number = plain[-1] * -1
        return plain[:pad_number]
    return plain

def decryption_oracle(cipher, key):
    decryption_suite = AES.new(key, AES.MODE_ECB)
    plain = decryption_suite.decrypt(cipher)
    return remove_padding(plain, len(key))

def profile_for(email):
    user = {'email': sanity_clean(email), 'uid' : UID, 'role': 'user' }
    return encryption_oracle(encode(user),'"provide" that to the "attacker"')


final_block = "root".encode() + bytes([28])*28 # make root the final block
prefix_length = len('email=')
email_length = 32 - prefix_length #prefix email with garbage so that we can append final block to it to get it encrypted as a single block
email_grabage = 'A'*email_length
email = email_grabage + final_block.decode()
cut = profile_for(email)[32:64] # final_block encrypted
original_cipher = profile_for("foo@baaaar.com") # the email has been curated in such a way that email=<email>&uid=<uid>& will be 32 bytes
morphed_cipher = decryption_oracle(original_cipher[0:32] + cut, '"provide" that to the "attacker"') #replacing the second part of the
print(parse_cookie(morphed_cipher.decode()))