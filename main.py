import socket
import sys

key = {
	"p" : 0,
	"q" : 0,
	"n" : 0,
	"e" : 0,
	"d" : 0,
}

key["p"] =  int(input("Enter RSA key p value: "))
key["q"] = int(input("Enter RSA key q value: "))
if key["p"] == key["q"]:
	print("Bad p or q.")
	exit(1)

find_n = lambda x, y: x * y

key["n"] = find_n(key["p"], key["q"])
if key["n"] < 255:
	print("Bad p or q.")
	exit(1)

gcd = lambda a, b : a if b == 0 else gcd(b, a % b)
lcm = lambda a, b : abs(a * b) / gcd(a, b)
is_coprime = lambda a, b: True if gcd(a, b) == 1 else False

find_e = lambda x, i: i if is_coprime(x, i) else find_e(x, i + 1)

lmbd = int(lcm(key["p"] - 1, key["q"] - 1))
e = find_e(lmbd, 3)
if e > lmbd:
	print("Bad p or q.")
	exit(1)
key["e"] = e

# IMPORTANT
sys.setrecursionlimit(10000)

factorial = lambda a, counter : a if counter <= 0 else factorial(a * counter, counter - 1)
ret_if_div = lambda x, a : x if x % a == 0 else 0
ret_if_prime = lambda x : x if factorial(1, x - 1) % x == -1 % x else 0
# always call with (number, 1, 2)
phi = lambda x, acc, counter : int(x * acc) if counter > x else phi(x, acc * (1 - 1 / counter), counter + 1) if ret_if_prime(counter) != 0 and ret_if_div(x, counter) != 0 else phi(x, acc, counter + 1)

find_d = lambda e, lmbd : e ** (phi(lmbd, 1, 2) - 1) % lmbd

key["d"] = int(find_d(key["e"], lmbd))

encrypt = lambda x : x ** key["e"] % key["n"]
decrypt = lambda x : x ** key["d"] % key["n"]

print("Public key: ", key["e"], " mod: ", key["n"])
print("Private key: ", key["d"], " mod: ", key["n"])
print("Ready.")

LOCALHOST = "127.0.0.1"
PORT = 8017

def decode(y):
	x = 0
	i = len(y) - 1
	while i >= 0:
		x <<= 8
		x |= y[i]
		i -= 1
	return x

def encode(x):
	ret = []
	while x:
		ret.append(x & 0xff)
		x >>= 8
	return bytearray(ret)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
	sock.bind((LOCALHOST, PORT))
	print("Listening for connections on port:", PORT)
	while True:
		data = sock.recv(1024)

		print(chr(decrypt(decode(data))), end="")
except:
	sock.connect((LOCALHOST, PORT))
	while True:
		message = bytearray(str(input("> ")) + "\n", "utf-8")
		for byte in message:
			sock.sendall(encode(encrypt(byte)))

		if message == b"exit\n":
			exit(0)