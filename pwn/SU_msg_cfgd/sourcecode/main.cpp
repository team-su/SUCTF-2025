#include <iostream>
#include <map>
#include <vector>
#include <cstring>
#include <cstdlib>
#include "mainLoop.hpp"
#include "msgHandler.hpp"

int main() {

    setbuf(stdin, 0LL);
    setbuf(stdout, 0LL);
    setbuf(stderr, 0LL);
    // 首先创建必要的对象
    MainLoop mainLoop;
    LocalHandler localHandler;
    RemoteHandler remoteHandler;

    // 将对应的handler进行注册
    mainLoop.handle_register(&localHandler, 0x41);
    mainLoop.handle_register(&remoteHandler, 0x61);

    // 调用looper，执行主要函数
    mainLoop.looper_start();

    return 0;
}