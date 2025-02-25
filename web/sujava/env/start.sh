#!/bin/bash

# 检查系统架构
ARCH=$(uname -m)

# 根据系统架构选择相应的 zip 包
if [ "$ARCH" == "x86_64" ]; then
 #   ZIP_FILE="/app/Java8_amd64.zip"
    Java="/app/Java8/bin/java"
elif [ "$ARCH" == "aarch64" ]; then
#    ZIP_FILE="/app/Java8_arch.zip"
    Java="/app/Java_8/bin/java"
else
    echo "Unsupported architecture: $ARCH"
    exit 1
fi

# 解压 zip 包
#unzip $ZIP_FILE -d /app/

# 执行其他操作，例如启动 Java 应用程序
$Java -jar /app/suJava-0.0.1-SNAPSHOT.jar
