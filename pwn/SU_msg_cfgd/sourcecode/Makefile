# 定义编译器
CXX = g++

# 定义编译选项
CXXFLAGS = -std=c++11 -Wall -Wextra

# 定义目标文件和源文件
TARGET = main
SRC = main.cpp
HEADERS = cmd.h config.h base_handler.h cmd.cpp mainLoop.hpp msgHandler.hpp
OBJS = main.o cmd.o

# 默认目标
all: $(TARGET)

# 生成目标文件
$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(OBJS)

# 生成目标文件的依赖关系
main.o: main.cpp $(HEADERS)
	$(CXX) $(CXXFLAGS) -c main.cpp

cmd.o: cmd.cpp cmd.h
	$(CXX) $(CXXFLAGS) -c cmd.cpp

# 清理生成文件
clean:
	rm -f $(OBJS) $(TARGET)

# 伪目标
.PHONY: all clean
