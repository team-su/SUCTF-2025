#ifndef _CMD_
#define _CMD_

#include<cstdlib>
#include<iostream>


#include"msg.h"

// 发生了对齐现象
struct CfgCMD {
    int type;
    struct {
        unsigned int length;
        char* config_name;
    } name;
    struct {
        unsigned int length;
        char* config_content;
    } content;
    bool updated;
};

struct CMD {
    int msg_type;
    int cmd_target;
    unsigned int cnt;
    char data[1]; // 实际上是一个可变长度数组，存放 CfgCMD 的数据
};


void* next_CfgCMD(CfgCMD* cfgCmd);
CfgCMD* parseTLVCfgCMD(char* tlvData);

#endif // _CMD_