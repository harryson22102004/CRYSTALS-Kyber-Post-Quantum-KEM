import numpy as np, os, hashlib
 
# Simplified Ring-LWE based KEM (educational, not production)
Q = 3329; N = 256; K = 2
 
def ntt_mul(a, b, q=Q):
    c = np.zeros(N, dtype=np.int64)
    for i in range(N):
        for j in range(N):
            sign = 1 if i+j < N else -1
            c[(i+j) % N] = (c[(i+j)%N] + sign*a[i]*b[j]) % q
    return c
 
def keygen():
    A  = np.random.randint(0, Q, (K,K,N), dtype=np.int64)
    s  = np.random.randint(-2, 3, (K,N), dtype=np.int64)
    e  = np.random.randint(-2, 3, (K,N), dtype=np.int64)
    pk = (A, (np.sum([ntt_mul(A[i][j], s[j]) for j in range(K)], axis=0)+e[0])%Q)
    sk = s
    return pk, sk
 
def encapsulate(pk):
    A, t = pk
     r  = np.random.randint(-2, 3, (K,N), dtype=np.int64)
    e1 = np.random.randint(-2, 3, (K,N), dtype=np.int64)
    e2 = np.random.randint(-2, 3, N, dtype=np.int64)
    m  = np.random.randint(0, 2, N, dtype=np.int64) * (Q//2)
    u  = (np.sum([ntt_mul(A[0][j], r[j]) for j in range(K)], axis=0)+e1[0])%Q
    v  = (np.sum([ntt_mul(t, r[j]) for j in range(K)], axis=0)+e2+m)%Q
    key = hashlib.sha256(m.tobytes()).hexdigest()
    return (u,v), key
 
pk,sk=keygen()
ct,shared_key=encapsulate(pk)
print(f"Ciphertext u shape: {ct[0].shape}")
print(f"Shared key: {shared_key[:32]}...")
