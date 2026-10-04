import hashlib
import os
import time

# Löesnordert som vi vill skapa en hash av.
# .encode()gör om texten från en vanlig sträng till bytes.
# Eftersom pbkdf2_hmac arbetar med bytes.
password = "Mittlösenord123".encode()

salt1 = os.urandom(16)
salt2 = os.urandom(16)

interations1 = 100_000
interations2 = 500_000

start = time.perf_counter() 

hash1 = hashlib.pbkdf2_hmac(
    "sha256"
    password,
    salt1,
    interations1,
)
time1 = time.perf_counter() - start

start = time.perf_counter()

hash2 = hashlib.pbkdf2_hmac(
    "sha256"
    password,
    salt2,
    interations1
)

time2 = time.perf_counter() - start

time = time.perf_counter()

hash3 = hashlib.pbkdf2_hmac(
    "sha256"
    password,
    salt1,
    interations2
)

time3 = time.perf_counter() - start

print("hash med salt 1:")
print(hash1.hex())

print()


