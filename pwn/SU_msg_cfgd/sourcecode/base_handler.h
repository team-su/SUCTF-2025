#ifndef _BASE_HANDLER
#define _BASE_HANDLER

#include<cstdlib>
#include<iostream>

class Handler {
public:
    virtual void handleMsg() = 0;
    virtual void handleCMD(char* msg) = 0;
    virtual void cmdGet(char* msg) = 0;
    virtual void cmdAdd(char* msg) = 0;
};
#endif // #ifndef _BASE_HANDLER