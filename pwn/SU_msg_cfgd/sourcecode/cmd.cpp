#include "cmd.h"
#include<unistd.h>
#include<cstdlib>
#include<string.h>

CfgCMD* parseTLVCfgCMD(char* tlvData) {
    CfgCMD* cfgCmd = new CfgCMD();

    // 解析 type
    cfgCmd->type = *reinterpret_cast<int*>(tlvData);
    tlvData += sizeof(int);

    // 解析 name 的长度和内容
    cfgCmd->name.length = *reinterpret_cast<unsigned int*>(tlvData);
    if (cfgCmd->name.length > 0x100) {
        std::cerr << "Config name length is too large!" << std::endl;
        
        delete cfgCmd;
        return nullptr;
    }
    tlvData += sizeof(unsigned int);

    cfgCmd->name.config_name = new char[cfgCmd->name.length + 1];
    memcpy(cfgCmd->name.config_name, tlvData, cfgCmd->name.length);
    cfgCmd->name.config_name[cfgCmd->name.length] = '\0';
    tlvData += cfgCmd->name.length;

    // 解析 content 的长度和内容
    cfgCmd->content.length = *reinterpret_cast<unsigned int*>(tlvData);
    if (cfgCmd->content.length > 0x1000) {
        std::cerr << "Config content length is too large!" << std::endl;
        delete[] cfgCmd->name.config_name;
        delete cfgCmd;
        return nullptr;
    }
    tlvData += sizeof(unsigned int);

    cfgCmd->content.config_content = new char[cfgCmd->content.length + 1];
    memcpy(cfgCmd->content.config_content, tlvData, cfgCmd->content.length);
    cfgCmd->content.config_content[cfgCmd->content.length] = '\0';
    tlvData += cfgCmd->content.length;

    // 解析 updated 标志
    cfgCmd->updated = *reinterpret_cast<bool*>(tlvData);

    return cfgCmd;
}


void* next_CfgCMD(CfgCMD* cfgCmd){

    return cfgCmd + sizeof(CfgCMD) - sizeof(unsigned int) * 2 + cfgCmd->name.length + cfgCmd->content.length;
}