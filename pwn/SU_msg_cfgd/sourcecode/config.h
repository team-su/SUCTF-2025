#ifndef __CONFIG_H_
#define __CONFIG_H_

#include <iostream>
#include <vector>
#include <cstring>

#include <cstring>

class Config {
public:
    int config_type;
    char* config_name;
    char* content;

    // 析构函数
    ~Config() {
        delete[] this->config_name;
        delete[] this->content;
    }

    // 构造函数
    Config(int type, const char* name, unsigned int name_len, const char* content, unsigned int content_len) {
        config_type = type;
        config_name = new char[name_len + 1];
        memcpy(config_name, name, name_len);
        config_name[name_len] = '\0';
        this->content = new char[content_len + 1];
        memcpy(this->content, content, content_len);
        this->content[content_len] = '\0';
    }
};

#endif // __CONFIG_H_