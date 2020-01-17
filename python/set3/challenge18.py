#!/bin/python3

from Crypto.Cipher import AES
from Crypto.Util import Counter
import base64

new_counter = Counter.new(8*8, prefix=b'\x00'*8, initial_value=0, little_endian=True)
Key = b'YELLOW SUBMARINE'
cipher = AES.new(Key, AES.MODE_CTR, counter=new_counter)
print(cipher.decrypt(base64.b64decode('L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ==')))