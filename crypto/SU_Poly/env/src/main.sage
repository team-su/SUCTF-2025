from Crypto.Util.number import *
from hashlib import md5
import signal
flag = b"SUCTF{bytes_to_long_of_SU_seems_bigger_than_19937_XD_try_random_matrix(GF(2),20000,20000)_and_see_its_rank!}"

PR.<x> = PolynomialRing(Zmod(0xfffffffffffffffffffffffffffffffe))
SUPOLY = PR.random_element(10)
gift = []
for i in range(bytes_to_long(b"SU")):
    f = PR.random_element(10)
    gift.append([int((f*SUPOLY)(j)) & 0xff for j in range(10)])
print("🎁 :", gift)

signal.alarm(10)
if(md5(str(SUPOLY.list()).encode()).hexdigest() == input("Show me :)")):
    print("🚩 :", flag)
else:
    print("🏳️ :", "flag")