from Crypto.Cipher import AES
import base64

def get_data(file_name):
    fd = open(file_name,'r')
    cont = fd.read()
    content = cont.replace('\n','')
    return base64.b64decode(content)

KEY = "YELLOW SUBMARINE"
decoder_suite = AES.new(KEY,AES.MODE_ECB)
print(decoder_suite.decrypt(get_data("7.txt")))
