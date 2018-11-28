#!/bin/python3
from Crypto.Cipher import AES
import random
import os
import base64
KEY = os.urandom(16)

def split(message, key_len):
    return [ message[i:i+key_len] for i in range(0, len(message), key_len)]

def pkcs_7_padding(message, key_len):
    ar = split(message, key_len)
    ar[-1] += bytes([key_len - len(ar[-1])]) * (key_len - len(ar[-1]))
    return ar


def encryption_oracle(message, over_ride=-1):
    text_padding_len = random.randint(5,10)
    text_padding_len_after = random.randint(5, 10)
    padding_after = os.urandom(text_padding_len_after)
    padding_before = os.urandom(text_padding_len)
    mode = random.randint(0,1)
    if over_ride == -1:
        print(mode)
    unknown_string = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"
    mesg = b"".join(pkcs_7_padding( message.encode() + base64.b64decode(unknown_string) ,16) )
    if (mode == 0 and over_ride == -1) or over_ride == 1:
        encryption_suite = AES.new(KEY, AES.MODE_ECB)
        cipher = encryption_suite.encrypt(mesg)
    if (mode == 1 and over_ride == -1) or over_ride == 2:
        IV = os.urandom(16)
        encryption_suite = AES.new(KEY, AES.MODE_CBC, IV)
        cipher = encryption_suite.encrypt(mesg)
    return cipher

def get_block_size():
    for i in [16,24,31]:
        plain_text = "a" ** (i*3)

def break_encryption(key_size):
    total_blocks = ""
    for blocks in range(0,9):
        previously_found = []
        for i in range(1,17):
            first_block = ('A' * (key_size-i))
            cipher_to_match = encryption_oracle(first_block, over_ride=1)[blocks*16:(blocks+1)*16]
            for j in range(0,127):
                new_block = (first_block + total_blocks + "".join(previously_found))[blocks*16:(blocks+1)*16] + chr(j)
                cmp_block = encryption_oracle(new_block, over_ride=1)[0:16]
                if (cmp_block == cipher_to_match):
                    previously_found.append(chr(j))
                    break
        total_blocks += ("".join(previously_found))
    print(total_blocks)


#print(encryption_oracle("", over_ride=1))
break_encryption(16)