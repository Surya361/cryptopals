#!/bin/bash

def split(message, key_len):
    return [ message[i:i+key_len] for i in range(0, len(message), key_len)]


def pkcs_7_padding(message, key_len):
    ar = split(message, key_len)
    ar[-1] += bytes([key_len - len(ar[-1])]) * (key_len - len(ar[-1]))
    return ar

def pkcs_7_stripper(message, key_len):
    if type(message[-1]) is int and message[-1] < key_len:
        pad_number = message[-1] * -1
        if len(message[pad_number:]) == message[-1] and len(set(message[pad_number:])) == 1:
            return message[:pad_number]
        else:
            raise Exception("Padding error")
print(pkcs_7_stripper(b'ICE ICE BABY\x01\x02\x03\x04',16))