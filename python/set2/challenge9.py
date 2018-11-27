def split(message, key_len):
    return [ message[i:i+key_len] for i in range(0, len(message), key_len)]


def pkcs_7_padding(message, key_len):
    ar = split(message, key_len)
    ar[-1] += str(key_len - len(ar[-1])) * (key_len- len(ar[-1]))
    return ar


print(pkcs_7_padding("HELLO WORLD",1))