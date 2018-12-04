#!/bin/python3
from Crypto.Cipher import AES
import random
import os
import base64
KEY = os.urandom(16)
prefix_len = random.randint(0,100)
RANDOM_PREFIX = os.urandom(prefix_len)

def split(message, key_len):
    return [ message[i:i+key_len] for i in range(0, len(message), key_len)]

def pkcs_7_padding(message, key_len):
    ar = split(message, key_len)
    ar[-1] += bytes([key_len - len(ar[-1])]) * (key_len - len(ar[-1]))
    return ar


def encryption_oracle(message, over_ride=-1):
    mode = random.randint(0,1)
    if over_ride == -1:
        print(mode)
    mesg = b"".join(pkcs_7_padding(format_string(message) ,16) )
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

def format_string(message):
    unknown_string = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"
    return RANDOM_PREFIX + message.encode() + base64.b64decode(unknown_string)

def break_encryption(key_size):
    total_blocks = ""
    garbage_len = get_initial_random_size(key_size)
    remove_blocks = ((garbage_len % key_size) + 1)
    sanity_size = (remove_blocks * key_size) - garbage_len
    for blocks in range(0,9):
        previously_found = []
        for i in range(1,17):
            sanity_block = 'A' * sanity_size
            first_block = sanity_block + ('A' * (key_size-i))
            unclean_cipher = encryption_oracle(first_block, over_ride=1)
            clean_cipher = unclean_cipher[remove_blocks*key_size:]
            cipher_to_match = clean_cipher[blocks*16:(blocks+1)*16]
            for j in range(0,127):
                new_block = (first_block + total_blocks + "".join(previously_found)) + chr(j)
                cmp_block_unclean = encryption_oracle(new_block, over_ride=1)
                cmp_block_clean = cmp_block_unclean[remove_blocks*key_size:]
                cmp_block = cmp_block_clean[blocks*16:(blocks+1)*16]
                #print(cmp_block, cipher_to_match, first_block, new_block)
                if (cmp_block == cipher_to_match):
                    previously_found.append(chr(j))
                    break
        total_blocks += ("".join(previously_found))
    print(total_blocks)


def get_initial_random_size(key_size):
    two_blocks_similar = 'A' * (2*key_size)
    for i in range(0,17):
        final_message = ('A'*i) + two_blocks_similar
        cipher = encryption_oracle(final_message, over_ride=1)
        cipher_block_array = split(cipher,key_size)
        cmp = [b'']
        for cipher_block in cipher_block_array:
            if cipher_block == cmp:
                return (cipher_block_array.index(cipher_block)*16) - i
            cmp = cipher_block


#print(get_initial_random_size(16))
break_encryption(16)
#print(encryption_oracle("", over_ride=1))
#break_encryption(16)