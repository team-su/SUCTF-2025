#include <iostream>
#include <vector>
#include <map>
#include <cstring>
#include <unistd.h>
#include "base_handler.h"
#include "config.h"
#include "cmd.h"

class MainLoop : public Handler {
public:

    std::map<int, Handler*> msg_queue;
    std::vector<Config*> cmd_queue;
    std::vector<CfgCMD*> cfgcmd_queue;

    MainLoop()
    {
        cmd_queue.reserve(1);
        cfgcmd_queue.reserve(1);
    }
    void handle_register(Handler* hd, int handle_id) {
        msg_queue[handle_id] = hd;
    }

    void handle_dispatch(char* msg) {
        CMD* cmd = reinterpret_cast<CMD*>(msg);
        auto it = msg_queue.find(cmd->cmd_target);
        if (it != msg_queue.end()) {
            it->second->handleCMD(msg);
        } else {
            std::cerr << "Undefined Handler" << std::endl;
        }
    }

    void looper_start() {
        char msg[0x10000];
        while (true) {
            std::cout << "Enter command: ";
            // std::cin.read(msg, 0x1000);
            // std::streamsize bytesRead = std::cin.gcount();
            unsigned long bytesRead = read(0, msg, 0x10000);

            if (bytesRead >= sizeof(CMD)) {
                CMD* cmd = reinterpret_cast<CMD*>(msg);
                if(cmd->cnt > 0x30)
                {
                    std::cerr << "Too much cfg!" << std::endl;
                }

                // if(cfgcmd_queue.size() > 0x30)
                // {
                //     std::cerr << "Too much CMD!" << std::endl;
                // }

                CMD* cmdStruct = reinterpret_cast<CMD*>(cmd);
                unsigned int actualSize = sizeof(int)*3 + 1;

                char* cmdData = cmdStruct->data;
                for (unsigned int i = 0; i < cmdStruct->cnt; ++i) {
                    CfgCMD* cfgCmd = parseTLVCfgCMD(cmdData);
                    if(cfgCmd == nullptr)
                    {
                        std::cerr << "Invalud TLV cfg!" << std::endl;
                        break;
                    }

                    cfgcmd_queue.push_back(cfgCmd);
                    unsigned int cfgCmdSize = sizeof(int)*2 + sizeof(int) + sizeof(bool) + cfgCmd->name.length + cfgCmd->content.length;
                    actualSize += cfgCmdSize;
                    cmdData += cfgCmdSize;
                    
                }

                if (bytesRead == actualSize) {
                    handleCMD(msg);
                    // here delete all cfgcmd
                    for (auto& cmd : cfgcmd_queue) {
                        delete [] cmd->content.config_content;
                        delete [] cmd->name.config_name;
                        delete cmd; // 这会调用CfgCMD的析构函数，进而释放Config的内存
                    }
                    cfgcmd_queue.clear(); // 清空向量
                } else {
                    std::cerr << "Invalid CMD size" << std::endl;
                }
            } else {
                std::cout << "Received data too small, just exit program" << std::endl;
                exit(0);
                break;
            }
        }
    }

    void handleMsg() override {
        // Implementation is not required
    }

    void handleCMD(char* msg) override {
        CMD* cmd = reinterpret_cast<CMD*>(msg);
        CfgCMD* cmdData = NULL;
        if (cmd->msg_type == 1) {
            handle_dispatch(msg);
        } else if (cmd->msg_type == 2) {
            // cmdData = reinterpret_cast<CfgCMD*>(cmd->data);
            for (unsigned int i = 0; i < cfgcmd_queue.size(); ++i) {
                cmdData = cfgcmd_queue[i];
                switch (cmdData->type) {
                case 0:
                    cmdGet(reinterpret_cast<char*>(cmdData));
                    break;
                case 1:
                    cmdAdd(reinterpret_cast<char*>(cmdData));
                    break;
                default:
                    std::cerr << "Invalid command type" << std::endl;
                }
                // cmdData = reinterpret_cast<CfgCMD*>(next_CfgCMD(cmdData));
            }
        } else {
            std::cerr << "Invalid msg_type" << std::endl;
        }
    }

    void cmdGet(char* msg) override {
        for (const auto& cfg : cmd_queue) {
            std::cout << "Config Name: " << cfg->config_name << ", Content: " << cfg->content << std::endl;
        }
    }

    void cmdAdd(char* msg) override {
        CfgCMD* cfg = reinterpret_cast<CfgCMD*>(msg);
        char* name = new char[cfg->name.length + 1];
        memcpy(name, cfg->name.config_name, cfg->name.length);
        name[cfg->name.length] = '\0';

        char* content = new char[cfg->content.length + 1];
        memcpy(content, cfg->content.config_content, cfg->content.length);
        content[cfg->content.length] = '\0';

        Config* newConfig = new Config(cfg->type, name, cfg->name.length, content, cfg->content.length);
        cmd_queue.push_back(newConfig);

        delete[] name;
        delete[] content;
    }
};