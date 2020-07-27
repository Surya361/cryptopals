import os, base64
from Crypto.Cipher import AES
from Crypto.Util import Counter


def encrypt(messgage: bytes, Key: bytes) -> bytes:
    counter = Counter.new(8*8, prefix=b'\x00'*8, initial_value=0, little_endian=True)
    encryption_oracle = AES.new(Key, AES.MODE_CTR, counter=counter)
    return encryption_oracle.encrypt(messgage)

def main():
    Key = os.urandom(16)
    fd = open("19.txt")
    plain = b''
    for line in fd:
        plain += encrypt(base64.b64decode(line)[0:16], Key)
    print(base64.b64encode(plain).decode()) #use the result as an input to repating key xor from set1/challenge6

if __name__ == "__main__":
    main()
