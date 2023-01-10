
import math as m
import numpy as np
import random

def find_s(n):
    count = 0
    temp = n - 1
    flag = 0
    if n%2 == 0:
        return False,0
    else:
        while flag == 0:
            temp /= 2
            count+=1
            if temp%2 == 1:
                break
    return count,int((n-1)/(2**count))

def miller_rabin_test(n: int):
    x = 0
    k = 400
    s,t = find_s(n)
    if not(s):
        return True
    for i in range(k):
        a = random.randrange(2, n-2)
        x = pow(a, t, n)
        if x == 1 or x == n-1:
            continue
        for i in range(s-1):
            x = (x**2) % n
            if x == 1:
                return False
            if x == n-1:
                break
        if x==n-1:
            continue
        return False
    return True

def gen_pr():
    n_0 = 2**32+1
    n_1 = int((2**64 - 2**32)/2)
    for i in range(0,n_1):
        x = random.randrange(n_0, n_1)
        if x%2 == 0:
            x+=1
        x+=2*i
        if miller_rabin_test(x):
            break
    return x

def gen_keys():
    p,q,p_1,q_1 = 1,1,1,1
    while p*q >= p_1 * q_1:
        p_1 = gen_pr()
        q_1 = gen_pr()
        p = gen_pr()
        q = gen_pr()
    return p, q, p_1, q_1

def fi_n(p: int, q: int):
    return (p - 1) * (q - 1)

def key_generation(p: int, q: int):
    n = p * q
    e = pow(2, 16) + 1 # 2<= e <= (n - 1), gcd(e, fi_n) == 1
    d = pow(e, -1, fi_n(p, q)) # de = 1(mod(fi_n))
    return [(d, p, q), (n, e)]

def encryption(M, ne):
    n, e = ne[0], ne[1]
    return pow(M, e, n)

def decryption(C, dpq):
    d = dpq[0]
    n = dpq[1] * dpq[2]
    return pow(C, d, n)

def digital_signification(M, dpq):
    d, n = dpq[0], dpq[1] * dpq[2]
    return (M, pow(M, d, n))

def verify(MS, ne):
    M, S = MS[0], MS[1]
    n, e = ne[0], ne[1]
    return M == pow(S, e, n)    

def send_message(M):
    p,q,p_1,q_1 = gen_keys()
    keys_A = key_generation(p,q)
    C = encryption(M, keys_A[1])
    print("Send message: ", C, "\nKeys:", keys_A[0])
    return C, keys_A[0]

def read_message(C, keys):
    Message = decryption(C, keys)
    return Message

class mes():
    def __init__(self, name,p,q):
        self.name = name
        self.p = p
        self.q = q
    def gen_data(self):
         self.k = random.randrange(0, 2**32)
         self.k_1 = pow(self.k,self.e_1,self.n_1)
         self.S = pow(self.k,self.keys[0][0],self.keys[1][0])
         self.S_1 = pow(self.S,self.e_1,self.n_1)
    def verify(self, k, S):
        k_ver = pow(S, self.keys[1][1],self.keys[1][0])
        return k_ver == k
    def get_data(self, k_1, S_1):
        k = pow(k_1, self.keys_first[0][0], self.keys_first[1][0])
        S = pow(S_1, self.keys_first[0][0], self.keys_first[1][0])
        return k,S
    def get_open_key(self, e_1, n_1):
        self.e_1 = e_1
        self.n_1 = n_1
    def gen_keys(self):
        self.keys = key_generation(self.p,self.q)
        while self.keys[1][0] >= self.n_1:
            print(self.keys[1][0], self.n_1)
            self.keys = key_generation(self.p,self.q)
    def gen_first_keys(self):
        self.keys_first = key_generation(self.p,self.q)
def main():
    M = random.randrange(0, 2**32)
    print("Generate_message: ", M)
    cr_mess, k = send_message(M)
    M_decr = decryption(cr_mess, k)
    print("Decryption message:", M_decr)

    print("===========================")
    M = random.randrange(0, 2**32)
    print("Generate_message: ", M)
    p,q = gen_keys()[0:2]
    keys = key_generation(p,q)
    dig_sign = digital_signification(M,keys[0])
    print("Digital signification:", dig_sign)
    print("Verification:",verify(dig_sign,keys[1]))
    print("===========================")
    print("Send keys")
    p,q,p_1,q_1 = gen_keys()
    A = mes("A",p,q)
    B = mes("B",p_1,q_1)
    B.gen_first_keys()
    A.get_open_key(B.keys_first[1][1], B.keys_first[1][0])
    A.gen_keys()
    A.gen_data()
    k,S = B.get_data(A.k_1,A.S_1)
    print(A.verify(k,S))
main()
