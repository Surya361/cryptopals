from Crypto.Cipher import AES
import base64
import os
import random
import time

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
    key = os.urandom(16)
    mode = random.randint(0,1)
    if over_ride == -1:
        print(mode)
    mesg = b"".join(pkcs_7_padding(padding_before + message.encode() + padding_after,16) )
    if (mode == 0 and over_ride == -1) or over_ride == 1:
        encryption_suite = AES.new(key, AES.MODE_ECB)
        cipher = encryption_suite.encrypt(mesg)
    if (mode == 1 and over_ride == -1) or over_ride == 2:
        IV = os.urandom(16)
        encryption_suite = AES.new(key, AES.MODE_CBC, IV)
        cipher = encryption_suite.encrypt(mesg)
    #return base64.b64encode(cipher)
    return cipher

def detect_common():
    plain_text = "a"*100000000
    start_time = time.time()
    cipher_text = encryption_oracle(plain_text)
    end_time = time.time()
    a = split(cipher_text,16)
 #   print(a)
    if a[1] == a[2]:
        print("ecb")
    else:
        print("cbc")
    print(end_time-start_time)

def get_times():
    message = "a" * 100000000
    start_time = time.time()
    cipher = encryption_oracle(message, over_ride=1)
    end_time = time.time()
    ecb_time = end_time - start_time
    start_time = time.time()
    cipher = encryption_oracle(message, over_ride=2)
    end_time = time.time()
    cbc_time = end_time - start_time
    return ecb_time, cbc_time

def side_channel_detect(cbc_time,ecb_time):
    """this is a side channel determination, works on parallelizability of cbc and ecb
        it requires low noise and big input to accurately determine
    """
    plain_text = "a" * 100000000
    margin = cbc_time-ecb_time
    if margin < 0:
        print("system noise side channel not possible")
        exit(1)
    else:
        start_time = time.time()
        encryption_oracle(plain_text)
        end_time = time.time()
        print(end_time)
        if (end_time - start_time) < (ecb_time + margin/2):
            print("ecb")
        else:
            print("cbc")



#print(encryption_oracle("yellow submarine"))
ecb_time,cbc_time = get_times()
print(cbc_time,ecb_time)
side_channel_detect(cbc_time,ecb_time)
#for i in range(1,10):
#    detect_common()
