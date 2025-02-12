import numpy as np
import random
from math import sqrt

# Global variables
XA = 1
q = 1
a = 1

def setXA(num):
    global XA
    XA = num

def getXA():
    return XA

def setq(num):
    global q
    q = num

def getq():
    return q

def seta(num):
    global a
    a = num

def geta():
    return a

def power(x, y, p):
    res = 1  # Initialize result
    x = x % p  # Update x if it is more than or equal to p

    while y > 0:
        # If y is odd, multiply x with result
        if y & 1:
            res = (res * x) % p
        # y must be even now
        y = y >> 1  # y = y/2
        x = (x * x) % p

    return res

def findPrimefactors(s, n):
    # Print the number of 2s that divide n
    while n % 2 == 0:
        s.add(2)
        n = n // 2

    # n must be odd at this point. So we can skip one element (Note i = i +2)
    for i in range(3, int(sqrt(n)), 2):
        # While i divides n, print i and divide n
        while n % i == 0:
            s.add(i)
            n = n // i

    # This condition is to handle the case when n is a prime number greater than 2
    if n > 2:
        s.add(n)

def findPrimitive(n):
    s = set()
    phi = n - 1
    findPrimefactors(s, phi)

    for r in range(2, phi + 1):
        flag = False
        for it in s:
            if power(r, phi // it, n) == 1:
                flag = True
                break
        if not flag:
            return r
    return -1

def generate_public_key():
    global q, a, XA
    while True:
        q = random.randrange(100, 999)
        i = q - 1
        ct = 0

        while i >= 5:
            if q % i == 0:
                ct += 1
                break
            i -= 1

        if ct == 0:
            print("Prime random number q generated:", q)
            break

    a = findPrimitive(q)
    seta(a)
    print("Primitive root a:", a)

    XA = random.randrange(0, q - 1)
    setXA(XA)
    print("Private key XA generated:", XA)

    YA = power(a, XA, q)
    print("Public key YA generated:", YA)

    publickey = [q, a, YA, XA]
    return publickey

def encrypt_gamal(q, a, YA, text):
    print("=======================================> Start ElGamal encryption")
    text = list(text)
    asc = [ord(char) for char in text]

    k = random.randrange(0, q)
    print("Random integer k generated:", k)

    K = power(YA, k, q)
    print("K =", K)

    C1 = power(a, k, q)
    print("Generated Cipher 1 (C1):", C1)

    C2 = [(K * M) % q for M in asc]
    print("Generated Cipher 2 (C2):", C2)

    returnedvalue = f"{C1}," + ",".join(map(str, C2)) + f",{q}"
    print("Returned value:", returnedvalue)
    return returnedvalue

def decrypt_gamal(messagecopy, XA):
    print("======================================================> Start decryption")
    tempmessage = messagecopy.split(",")
    C1 = int(tempmessage[0])
    q = int(tempmessage[-1])
    C2 = [int(i) for i in tempmessage[1:-1]]

    print("Received Cipher 1 (C1):", C1)
    print("Received Cipher 2 (C2):", C2)

    K = power(C1, XA, q)
    print("K =", K)

    kinverse = 1
    while (kinverse * K) % q != 1:
        kinverse += 1

    print("K inverse:", kinverse)

    output = [(C2_i * kinverse) % q for C2_i in C2]
    print("Decrypted output:", output)

    decryptedText = "".join([chr(i) for i in output])
    print("Decrypted Text:", decryptedText)
    return decryptedText

# Example usage
publickey = generate_public_key()
q, a, YA, XA = publickey

text = "HELLO"
encrypted_message = encrypt_gamal(q, a, YA, text)
decrypted_message = decrypt_gamal(encrypted_message, XA)