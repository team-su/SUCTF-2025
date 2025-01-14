from Crypto.Util.number import *
from pwn import *

class myhash:
    def __init__(self,n):
        self.g = 91289086035117540959154051117940771730039965839291520308840839624996039016929
        self.n = n

    def update(self,msg: bytes):
        for i in range(len(msg)):
            self.n = self.g * (2 * self.n + msg[i])
            self.n = self.n & ((1 << 383) - 1)

    def digest(self) -> bytes:
        return long_to_bytes((self.n - 0xd1ef3ad53f187cc5488d19045) % (1 << 128))
    
    def getn(self):
        return self.n
io = remote("1.95.46.185",10007)
from hashlib import sha256
import string
from tqdm import tqdm
s = io.recvline().decode().replace("\n","")
ss = s.split("+")[2].split(")")[0].encode()
sss = s.split(" == ")[1]
io.recv()
for i in tqdm(string.ascii_letters + string.digits):
    for j in string.ascii_letters + string.digits:
        for m in string.ascii_letters + string.digits:
            for n in string.ascii_letters + string.digits:
                temp1 = i + j +m +n
                temp = temp1.encode() + ss
                if sha256(temp).hexdigest() == sss:
                    io.sendline(temp1.encode())
                    break
io.recvuntil(b' = ')
n0 = int(io.recvuntil(b'\n',drop=True).decode())
print(n0)
def fn(msg,n0):
    h = myhash(n0)
    ret = bytes([0] * 16)
    for b in msg:
        h.update(bytes([b]))
        ret = xor(ret,h.digest())
    return ret

def has(msg):
    h = myhash(n0)
    for b in msg:
        h.update(bytes([b]))
    return h.digest()
def byt2bv(b, n):
    b = [int(i) for i in bin(bytes_to_long(b))[2:].zfill(128)]
    return vector(GF(2), b)

def xor(x, y):
    x = b'\x00'*(16-len(x)) + x 
    y = b'\x00'*(16-len(y)) + y 
    return long_to_bytes(bytes_to_long(bytes([a ^^ b for a, b in zip(x, y)])))
g = 91289086035117540959154051117940771730039965839291520308840839624996039016929
c = 64
M=Matrix(ZZ,c+1,c+1)
for i in range(c):
    M[i,i]=1
    M[i,c]=(2*g)^(c-1-i) %(2^128)
M[c,c]=2^128
res=M.LLL()
ma = []
mb = []
for k in range(125,132):
    for r in res[1:-1]:
        m = b''
        for i in range(len(r[:-1])):
            m += long_to_bytes(k+r[i])
        if (has(m)==has(long_to_bytes(k)*64)):
            ma.append(long_to_bytes(k)*64)
            mb.append(m)
xs = []
ms = []
prev = b''
for maa,mbb in zip(ma,mb):
    ms.append((maa, mbb))
    x = xor(fn(prev + maa,n0), fn(prev + mbb,n0))
    xs.append(x)
    prev += maa
cur = byt2bv(fn(b"".join(ma),n0), 128)
mat = matrix(GF(2), [byt2bv(x, 128) for x in xs])
assert mat.rank() == 128
target = byt2bv(b"justjusthashhash", 128)
# cur+?*mat=target
sol = mat.solve_left(target - cur)
# print(sol)
msg = b""
for v, maa, mbb in zip(sol, *zip(*ms)):
    if v == 0:
        msg += maa
    else:
        msg += mbb
print(fn(msg,n0) == b'justjusthashhash')
io.recvuntil(b'->')
print(len(msg.hex().encode()))
io.sendline(msg.hex().encode())
print(io.recv())