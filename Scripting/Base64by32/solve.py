from base64 import b64decode

with open('./base64by32','r') as encoded:
	string = encoded.read()
	
for i in range(32):
	string = b64decode(string)
	
print(string)
