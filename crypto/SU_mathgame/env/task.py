import socketserver
import signal
from Crypto.Util.number import *
from random import randint
import time
from sage.geometry.hyperbolic_space.hyperbolic_isometry import moebius_transform
from secret import flag

banner = br'''
 _____ ______   ________  _________  ___  ___          ________  ________  _____ ______   _______      
|\   _ \  _   \|\   __  \|\___   ___\\  \|\  \        |\   ____\|\   __  \|\   _ \  _   \|\  ___ \     
\ \  \\\__\ \  \ \  \|\  \|___ \  \_\ \  \\\  \       \ \  \___|\ \  \|\  \ \  \\\__\ \  \ \   __/|    
 \ \  \\|__| \  \ \   __  \   \ \  \ \ \   __  \       \ \  \  __\ \   __  \ \  \\|__| \  \ \  \_|/__  
  \ \  \    \ \  \ \  \ \  \   \ \  \ \ \  \ \  \       \ \  \|\  \ \  \ \  \ \  \    \ \  \ \  \_|\ \ 
   \ \__\    \ \__\ \__\ \__\   \ \__\ \ \__\ \__\       \ \_______\ \__\ \__\ \__\    \ \__\ \_______\
    \|__|     \|__|\|__|\|__|    \|__|  \|__|\|__|        \|_______|\|__|\|__|\|__|     \|__|\|_______|

'''
welcome = b"\nWelcome to my math game, let's start now!\n"


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

    def recv(self, prompt=b'SERVER <INPUT>: '):
        self.send(prompt, newline=False)
        return self._recvall()

    def game1(self):
        self.send(b"\nLet's play the game1!")
        rounds = 1000
        pseudo_prime = int(self.recv(prompt=b'[+] Plz Tell Me your number: '))
        if isPrime(pseudo_prime):
            self.send(b"\nNo! it's a prime, go away!")
            self.request.close()
        for i in range(rounds):
            if pow(randint(2, pseudo_prime), pseudo_prime - 1, pseudo_prime) != 1:
                self.send(b"\nYou failed in round " + str(i + 1).encode() + b', bye~~')
                self.request.close()
        self.send(b"\nCongratulations, you have won the game1!\n")
        return True

    def game2(self):
        self.send(b"Let's play the game2!")
        res = self.recv(prompt=b'[+] Plz give Me your a, b, c: ')
        a,b,c = [int(x) for x in res.split(b',')]
        try:
            assert (isinstance(a, int) and isinstance(a, int) and isinstance(c, int))
            assert a > 0
            assert b > 0
            assert c > 0
            assert a / (b + c) + b / (a + c) + c / (a + b) == 4
            assert int(a).bit_length() > 900 and int(a).bit_length() < 1000
            assert int(b).bit_length() > 900 and int(b).bit_length() < 1000
            assert int(c).bit_length() > 900 and int(c).bit_length() < 1000
            self.send(b"\nCongratulations, you have won the game2!\n")
            return True
        except:
            self.send(b"\nNo! Game over!")
            self.request.close()

    def final_game(self):
        self.send(b"Let's play the game3!")
        set_random_seed(int(time.time()))
        C = ComplexField(999)
        M = random_matrix(CC, 2, 2)
        Trans = lambda z: moebius_transform(M, z)
        out = []
        for _ in range(3):
            x = C.random_element()
            out.append((x,Trans(x)))
        out = str(out).encode()
        self.send(out)
        kx = C.random_element()
        kx_str = str(kx).encode()
        self.send(kx_str)
        C2 = ComplexField(50)
        ans = C(self.recv(prompt=b'[+] Plz Tell Me your answer: ').decode())
        if C2(ans) == C2(Trans(kx)):
            self.send(b"\nCongratulations, you have won the game3!")
            self.send(flag)
            self.request.close()
        else:
            self.send(b"\nNo! Game over!")
            self.request.close()

    def handle(self):
        signal.alarm(300)
        self.send(banner)
        self.send(welcome)
        step1 = self.game1()
        if not step1:
            self.request.close()
        step2 = self.game2()
        if not step2:
            self.request.close()
        self.final_game()


class ThreadedServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class ForkedServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = '0.0.0.0', 10001
    print("HOST:POST " + HOST+":" + str(PORT))
    server = ForkedServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    server.serve_forever()