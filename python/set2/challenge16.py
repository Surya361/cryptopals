#!/bin/python3
from Crypto.Cipher import AES
import os
import urllib.parse
import base64

KEY= os.urandom(16)
IV = os.urandom(16)
def create_plain_text( s:str ) -> bytes:
    return ("comment1=cooking%20MCs;userdata=" + urllib.parse.quote(s) +";comment2=%20like%20a%20pound%20of%20bacon").encode()

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
        print(len(message[pad_number:]) , message[-1],len(set(message[pad_number:])) )
        if len(message[pad_number:]) == message[-1] and len(set(message[pad_number:])) == 1:
            return message[:pad_number]
    raise Exception("Padding error")

def encryption_oracle(message:str) -> bytes:
    msg = b"".join(pkcs_7_padding(create_plain_text(message), 16))
    encryption_suite = AES.new(KEY, AES.MODE_CBC, IV)
    return encryption_suite.encrypt(msg)

def decryption_oracle(cipher:bytes) -> list:
    decryption_suite = AES.new(KEY, AES.MODE_CBC, IV)
    plain = pkcs_7_stripper(decryption_suite.decrypt(cipher), 16)
    return b';admin=true;' in plain

def replace(msg:bytes, new:bytes, index:int) -> bytes:
    return msg[:index] + new + msg[index+1:]

raw= encryption_oracle("AAadminAtrueA")
encoded= base64.b64encode(raw)
replace_semi = bytes([(ord('A') ^ raw[17]) ^ ord(';')])
replace_equal = bytes([(ord('A') ^ raw[23]) ^ ord('=')])
replace_semi2 = bytes([(ord('A') ^ raw[28]) ^ ord(';')])

print(decryption_oracle(replace(replace(replace(raw, replace_semi, 17), replace_semi2, 28), replace_equal, 23)))

