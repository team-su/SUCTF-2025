from Crypto.Cipher import AES
from ast import literal_eval
from hashlib import md5
import subprocess

ells = [*primes(3, 200), 269]
p = 4*prod(ells) - 1
F = GF(p)

SUKEY = [randint(-3, 3) for _ in range(len(ells))]
def SuAuth(A, priv, LIMIT=True):
    if any(priv[i] == SUKEY[i] for i in range(len(ells))) and LIMIT: return "🙅SUKEY"
    E = EllipticCurve(F, [0, A, 0, 1, 0])
    for sgn in [1, -1]:
        for e, ell in zip(priv, ells):
            for i in range(sgn * e):
                while not (P := (p + 1) // ell * E.random_element()) or P.order() != ell:
                    pass
                E = E.isogeny_codomain(P)
        E = E.quadratic_twist()
    return E.montgomery_model().a2()

cipher = lambda key: AES.new(md5(key.encode()).digest(),AES.MODE_ECB)
SUDOOR = cipher(str(SuAuth(0, SUKEY, 0))).encrypt(b"./OPEN_THE_FLAG!")
print("😜", SuAuth(0, SUKEY, 0))

while True:
    AKey = SuAuth(0, literal_eval(input("🔑: ")))
    try: subprocess.run(cipher(str(AKey)).decrypt(SUDOOR))
    except: continue