from pwn import *
from tqdm import tqdm
import time

io = process(["sage", "task.sage"])
ells = [*primes(3, 200), 269]

def guess(i):
    for j in range(-3, 4):
        io.sendline(str([4]*i+[j]+[4]*(len(ells)-i-1)))
        start = time.time()
        io.recvuntil("🔑: ")
        end = time.time()
        if end-start < 0.1:
            print("FIND: ", j)
            return j

io.recvuntil("🔑: ")
SUKEY = []
for _ in tqdm(range(len(ells))):
    SUKEY.append(guess(_)+3)

io.sendline(str(SUKEY))
io.interactive()