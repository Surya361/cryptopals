#!/bin/python3
import os
import base64
from Crypto.Cipher import AES

def encrypt() -> tuple:
    global Key
    Key = os.urandom(16)
    Iv = os.urandom(16)
    encryption_oracle = AES.new(Key, AES.MODE_CBC, Iv)
    cipher = encryption_oracle.encrypt(b''.join(pkcs_7_padding(randStr(), 16)))
    return cipher,Iv

def xor(b1: bytes, b2: bytes) -> bytes:
    final = []
    for a,b in zip(b1, b2):
        final.append(bytes([a ^ b]))
    return b''.join(final)

def split(message:bytes, key_len:int) -> list:
    return [ message[i:i+key_len] for i in range(0, len(message), key_len)]

def pkcs_7_padding(message: bytes, key_len: int) -> list:
    ar = split(message, key_len)
    if len(message)%key_len != 0:
        ar[-1] += bytes([key_len - len(ar[-1])]) * (key_len - len(ar[-1]))
    else:
        ar.append(bytes([key_len])*key_len)
    return ar

def pkcs_7_stripper(message: bytes, key_len: int) -> bytes:
    if message[-1] <= key_len:
        pad_number = message[-1] * -1
        #print(len(message[pad_number:]) , message[-1],len(set(message[pad_number:])) )
        if len(message[pad_number:]) == message[-1] and len(set(message[pad_number:])) == 1:
            return message[:pad_number]
    raise Exception("Padding error")
def randStr() -> bytes:
    randStr = ['MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=',
     'MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=',
     'MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==',
     'MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==',
     'MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl',
     'MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==',
     'MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==',
     'MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=', 'MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=',
     'MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93']
    randNum =  int.from_bytes(os.urandom(1), byteorder='big')%len(randStr)
    #randNum = 3
    return base64.b64decode(randStr[randNum])

def decrypt(cipher: bytes, Iv: bytes) -> bool:
    decryption_oracle = AES.new(Key, AES.MODE_CBC, Iv)
    plain = decryption_oracle.decrypt(cipher)
    #print(split(plain, 16))
    try:
        pkcs_7_stripper(plain, 16)
        return True
    except:
        return False
def replace(msg:bytes, new:bytes, index:int) -> bytes:
    #print(len(msg), index, index+1)
    #print(msg, new, index)
    #print(len(msg[:index] + new + msg[index+1:]),msg[:index] + new + msg[index+1:] )
    return msg[:index] + new + msg[index+1:]


def padding_oracle(cipher: list, Iv: bytes) -> bytes:
    temp = cipher.copy()
    final = []
    final.append(temp.pop())
    temp.insert(0, iv)
    result =[]
    for blkNo in range(len(temp)-1):
        result.append(padding_oracle_helper(temp[blkNo:(blkNo+2)], Iv))
    #print(len(cipher))
    for blkNo in range(len(result)):
        print(xor(temp[blkNo], result[blkNo]))
    final.insert(0, temp.pop())
    print(xor(padding_oracle_helper_final(final, iv, []), final[0]))

def padding_oracle_helper(cipher: list, Iv: bytes) -> bytes:
    temp = cipher.copy()
    block = b'\x00'*16
    for j in range(15, -1, -1):
        found = b''
        for k in range(15, j, -1 ):
            #print(k)
            #print(block[k])
            temp[0] = replace(temp[0], bytes([(16-j) ^ block[k]]), k)
        for i in range(256):
            temp[0] = replace(temp[0], bytes([i]), j)
            #print(temp[0], len(temp[0]))
            if decrypt(b''.join(temp), Iv):
                found = bytes([i ^ (16-j)])
                #print(i,found, cipher[0])
                break
        #print("found", found)
        block = replace(block, found, j)
    return block

def padding_oracle_helper_final(cipher: list, Iv: bytes, ignore_list:list = []) -> bytes:
    temp = cipher.copy()
    block = b'\x00' * 16
    raw_i = [] + ignore_list
    for j in range(15, -1, -1):
        found = b''
        for k in range(15, j, -1):
            temp[0] = replace(temp[0], bytes([(16 - j) ^ block[k]]), k)
        for i in range(256):
            temp[0] = replace(temp[0], bytes([i]), j)
            if decrypt(b''.join(temp), Iv) and (i not in ignore_list):
                raw_i.append(i)
                found = bytes([i ^ (16 - j)])
                break
        if found == b'':
            ignore_list = raw_i
            print("recursion", raw_i)
            return padding_oracle_helper_final(cipher, Iv, ignore_list )
        block = replace(block, found, j)
    return block


ci, iv = encrypt()
k = split(ci, 16)
#print(k)
#print("IV",iv)
padding_oracle(k, iv)
#print(xor(padding_oracle_helper_final(k[1:3] , iv, []), k[1]))