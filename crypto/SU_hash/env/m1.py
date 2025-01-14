from hashlib import sha256
import socketserver
from Crypto.Util.number import *
import signal
import string
import random
import os

flag = "SUCTF{5imple_st4te_Tran3fer_w1th_s1m1lar_to_md5!!!!!}"
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

def fn(msg,n0):
    h = myhash(n0)
    ret = bytes([0] * 16)
    for b in msg:
        h.update(bytes([b]))
        ret = xor(ret,h.digest())
    return ret

class Task(socketserver.BaseRequestHandler):
    def _recvall(self):
        BUFF_SIZE = 2048
        data = b''
        while True:
            part = self.request.recv(BUFF_SIZE)
            data += part
            if len(part) < BUFF_SIZE:
                break
        return data.strip()

    def send(self, msg, newline=True):
        try:
            if newline:
                msg += b'\n'
            self.request.sendall(msg)
        except:
            pass

    def recv(self, prompt=b'[-] '):
        self.send(prompt, newline=False)
        return self._recvall()

    def proof_of_work(self):
        random.seed(os.urandom(8))
        proof = ''.join(
            [random.choice(string.ascii_letters+string.digits) for _ in range(20)])
        _hexdigest = sha256(proof.encode()).hexdigest()
        self.send(f"[+] sha256(XXXX+{proof[4:]}) == {_hexdigest}".encode())
        x = self.recv(prompt=b'[+] Plz tell me XXXX: ')
        if len(x) != 4 or sha256(x+proof[4:].encode()).hexdigest() != _hexdigest:
            return False
        return True
    

    
    def handle(self):
        
        signal.alarm(180)
        if not self.proof_of_work():
            self.send(b'[!] Wrong!')
            return
        n0 = 7771936934188215655661613361410686152210219325371595149904477566527822770739552753531404516579590316806865656619989
        self.send(b"n0 = " + str(n0).encode())
        self.send(b'"give me your msg ->"')
        try:
            your_input = bytes.fromhex(self.recv(prompt=b'give me your msg ->').decode().strip())
            # self.send(your_input.hex())
            print(fn(your_input,n0))
            if fn(your_input,n0) == b'justjusthashhash':
                self.send(flag.encode())
            else:
                self.send(b"try again?")
            return
        except:
            self.send(b"type error")
            return


class ThreadedServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class ForkedServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":
    HOST, PORT = '0.0.0.0', 10001
    server = ForkedServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    print(HOST, PORT)
    server.serve_forever()


    