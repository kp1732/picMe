# hasing lib
import hashlib
from hashlib import md5
from time import localtime


# will return SHA256 hashed + salted password string
def saltBae(password, salt):
	hashedPassword = hashlib.sha256((password+salt).encode("utf-8")).hexdigest()
	return hashedPassword

# will return SHA256 hashed + salted password string
def randFileName(filename):
	return "%s_%s" % (md5(str(localtime())).hexdigest(), filename)

file = open("names.txt", "r")

# for name in file.readlines():
# 	print(randFileName(name))+"\n"

print(saltBae("admin123", "cs3083"))