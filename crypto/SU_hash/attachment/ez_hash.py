from Crypto.Util.number import *

flag = b'SUCTF{??????????????????????????????}'

class myhash:
    def __init__(self,n):
        self.g = 91289086035117540959154051117940771730039965839291520308840839624996039016929
        self.n = n

    def update(self,msg: bytes):
        for i in range(len(msg)):
            self.n = self.g * (2 * self.n + msg[i])
            self.n = self.n & ((1 << 383) - 1)

    def digest(self) -> bytes:
        return ((self.n - 0xd1ef3ad53f187cc5488d19045) % (1 << 128)).to_bytes(16,"big")

def xor(x, y):
    x = b'\x00'*(16-len(x)) + x
    y = b'\x00'*(16-len(y)) + y
    return long_to_bytes(bytes_to_long(bytes([a ^ b for a, b in zip(x, y)])))

def fn(msg):
    n0 = getRandomNBitInteger(382)
    print(n0)
    h = myhash(n0)
    ret = bytes([0] * 16)
    for b in msg:
        h.update(bytes([b]))
        ret = xor(ret,h.digest())
    return ret

your_input = bytes.fromhex(input("give me your msg ->").strip())
if fn(your_input) == b'justjusthashhash':
    print(flag)
else:
    print("try again?")