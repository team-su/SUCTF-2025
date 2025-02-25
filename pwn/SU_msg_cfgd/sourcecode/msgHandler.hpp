#include <vector>
#include <algorithm>
#include "base_handler.h"
#include "config.h"
#include "cmd.h"

class MsgHandler : public Handler {
public:
    int handle_id;
    std::vector<Config*> vec_objs;
    std::vector<Config*>::iterator now_obj;
    std::vector<CfgCMD*> cfgcmd_queue;

    MsgHandler() : handle_id(-1), now_obj(vec_objs.end()) {
        vec_objs.reserve(1);
        cfgcmd_queue.reserve(1);
    }
    virtual ~MsgHandler() {
        for (auto cfg : vec_objs) {
            delete cfg;
        }
    }

    virtual void cmdUpdate(char* cmd) {
        CfgCMD* cfg = reinterpret_cast<CfgCMD*>(cmd);
        if (now_obj != vec_objs.end()) {
            delete[] (*now_obj)->config_name;
            delete[] (*now_obj)->content;
            (*now_obj)->config_name = new char[cfg->name.length + 1];
            memcpy((*now_obj)->config_name, cfg->name.config_name, cfg->name.length);
            (*now_obj)->config_name[cfg->name.length] = '\0';

            (*now_obj)->content = new char[cfg->content.length + 1];
            memcpy((*now_obj)->content, cfg->content.config_content, cfg->content.length);
            (*now_obj)->content[cfg->content.length] = '\0';
        }
    }

    virtual void add_obj(char* cmd) {
        CfgCMD* cfg = reinterpret_cast<CfgCMD*>(cmd);
        char* name = new char[cfg->name.length + 1];
        memcpy(name, cfg->name.config_name, cfg->name.length);
        name[cfg->name.length] = '\0';

        char* content = new char[cfg->content.length + 1];
        memcpy(content, cfg->content.config_content, cfg->content.length);
        content[cfg->content.length] = '\0';

        Config* newConfig = new Config(cfg->type, name, cfg->name.length, content, cfg->content.length);
        vec_objs.push_back(newConfig);

        delete[] name;
        delete[] content;
    }

    virtual void update_obj(char* cmd) {
        CfgCMD* cfg = reinterpret_cast<CfgCMD*>(cmd);
        for (auto it = vec_objs.begin(); it != vec_objs.end(); ++it) {
            if (strcmp((*it)->config_name, cfg->name.config_name) == 0) {
                delete[] (*it)->content;
                (*it)->content = new char[cfg->content.length + 1];
                strncpy((*it)->content, cfg->content.config_content, cfg->content.length);
                (*it)->content[cfg->content.length] = '\0';
                now_obj = it;
                return;
            }
        }
        add_obj(cmd);
    }

    virtual void visit_obj() {
        if (now_obj != vec_objs.end()) {
            printf("Current Object Name: %s \n", (*now_obj)->config_name);;
            printf("Content: %s\n",(*now_obj)->content);
        } else {
            puts("No current object.");
        }
    }

protected:

    virtual void handleCMD(char* cmd) override {
        CMD* cmdStruct = reinterpret_cast<CMD*>(cmd);
        // CfgCMD* cfgCmd = reinterpret_cast<CfgCMD*>(cmdStruct->data);
        char* cmdData = cmdStruct->data;
        for (unsigned int i = 0; i < cmdStruct->cnt; ++i) {
            CfgCMD* cfgCmd = parseTLVCfgCMD(cmdData);
            switch (cfgCmd->type) {
            case 0:
                cmdGet(reinterpret_cast<char*>(cfgCmd));
                break;
            case 1:
                cmdAdd(reinterpret_cast<char*>(cfgCmd));
                break;
            case 2:
                cmdUpdate(reinterpret_cast<char*>(cfgCmd));
                break;
            case 3:
                cmdDelete(reinterpret_cast<char*>(cfgCmd));
                break;
            case 4:
                cmdVisit(reinterpret_cast<char*>(cfgCmd));
                break;
            default:
                std::cerr << "Invalid command type" << std::endl;
            }
            
            if (cfgCmd->updated) {
                now_obj = std::find_if(vec_objs.begin(), vec_objs.end(),
                    [cfgCmd](Config* cfg) {
                        return strcmp(cfg->config_name, cfgCmd->name.config_name) == 0;
                    });
            }
            unsigned int cfgCmdSize = sizeof(int)*2 + sizeof(int) + sizeof(bool) + cfgCmd->name.length + cfgCmd->content.length;
            cmdData += cfgCmdSize;
            delete cfgCmd->name.config_name;
            delete cfgCmd->content.config_content;
            delete cfgCmd;
        }
    }

    virtual void cmdGet(char* cmd) override {

        CfgCMD* cfg = reinterpret_cast<CfgCMD*>(cmd);
        auto it = std::find_if(vec_objs.begin(), vec_objs.end(),
            [cfg](Config* config) {
                return strcmp(config->config_name, cfg->name.config_name) == 0;
            });

        if (it != vec_objs.end()) {
            std::cout << "Config Name: " << (*it)->config_name 
                      << ", Content: " << (*it)->content << std::endl;

        } else {
            std::cerr << "Configuration not found" << std::endl;
        }
    }

    virtual void cmdAdd(char* cmd) override{

        CfgCMD* cfg = reinterpret_cast<CfgCMD*>(cmd);
        auto it = std::find_if(vec_objs.begin(), vec_objs.end(),
            [cfg](Config* config) {
                return strcmp(config->config_name, cfg->name.config_name) == 0;
            });

        if (it != vec_objs.end()) {
            std::cout << "Config Exist " << std::endl;
            return;
        }

        if(vec_objs.size() > 0x30)
        {
            std::cerr << "Too much config!" << std::endl;
        }

        // CfgCMD* cfg = reinterpret_cast<CfgCMD*>(cmd);
        char* name = new char[cfg->name.length + 1];
        memcpy(name, cfg->name.config_name, cfg->name.length);
        name[cfg->name.length] = '\0';

        char* content = new char[cfg->content.length + 1];
        memcpy(content, cfg->content.config_content, cfg->content.length);
        content[cfg->content.length] = '\0';

        Config* newConfig = new Config(cfg->type, name, cfg->name.length, content, cfg->content.length);
        vec_objs.push_back(newConfig);

        delete[] name;
        delete[] content;
    }

    virtual void cmdDelete(char* cmd) {

        CfgCMD* cfg = reinterpret_cast<CfgCMD*>(cmd);
        auto it = std::find_if(vec_objs.begin(), vec_objs.end(),
            [cfg](Config* config) {
                return strcmp(config->config_name, cfg->name.config_name) == 0;
            });

        if (it != vec_objs.end()) {
            std::cout << "delete config " << (*it)->config_name << std::endl;

            delete *it;
            vec_objs.erase(it);
            
            return;
        }
    }

    virtual void cmdVisit(char* cmd) {
        if(now_obj != vec_objs.end())
        {
            visit_obj();
        }
    }
};

class LocalHandler : public MsgHandler {
public:
    void handleMsg() override {
        // 本地特定的消息处理逻辑
        std::cout << "Handling local message" << std::endl;
    }

    // virtual void cmdAdd(char* cmd) override {
    //     // 本地特定的设置命令处理逻辑
    //     CfgCMD* cfg = reinterpret_cast<CfgCMD*>(cmd);
    //     if (cfg->type == 0x1000)
    //     {
    //         std::cout << "Setting local config - Name: " << cfg->name.config_name 
    //                 << ", Content: " << cfg->content.config_content << std::endl;
    //         update_obj(cmd);
    //     }
    // }
};


class RemoteHandler : public MsgHandler {
public:
    void handleMsg() override {
        // 远程特定的消息处理逻辑
        std::cout << "Handling remote message" << std::endl;
    }

    virtual void cmdAdd(char* cmd) override {
        // 远程特定的设置命令处理逻辑
        CfgCMD* cfg = reinterpret_cast<CfgCMD*>(cmd);
        if (cfg->type !=2 )
        {
            std::cout << "Setting remote config - Name: " << cfg->name.config_name 
                    << ", Content: " << cfg->content.config_content << std::endl;
            update_obj(cmd);
        }
    }
};