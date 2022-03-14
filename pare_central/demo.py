

 
# we will be encryting the below string.
import base64


message = "hello geeks"
k = base64.urlsafe_b64encode(bytes(message,'utf-8'))
print(k)
print(base64.urlsafe_b64decode(str(k)).decode())
# generate a key for encryptio and decryption
# You can use fernet to generate
# the key or use random key generator
# here I'm using fernet to generate key
 
 
# then use the Fernet class instance
# to encrypt the string string must must
# be encoded to byte string before encryption

 
# print("original string: ", message)
# print("encrypted string: ", encMessage)
 
# decrypt the encrypted string with the
# Fernet instance of the key,
# that was used for encrypting the string
# encoded byte string is returned by decrypt method,
# so decode it to string with decode methods
# print(decMessage)