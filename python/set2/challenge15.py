#!/bin/bash

def split(message, key_len):
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
a = pkcs_7_padding(b'    ICE ICE BABY', 16)
print(pkcs_7_stripper(b"".join(a), 16))