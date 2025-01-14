#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

#define MAX_FLAG_LENGTH 100

int main() {
    char flag[MAX_FLAG_LENGTH];
    FILE *flag_file;

    // 检查是否有适当的权限
    if (geteuid() != 0) {
        printf("Error: Insufficient permissions\n");
        return 1;
    }

    // 打开并读取flag文件
    flag_file = fopen("/flag", "r");
    if (flag_file == NULL) {
        printf("Error: Unable to open flag file\n");
        return 1;
    }

    if (fgets(flag, MAX_FLAG_LENGTH, flag_file) == NULL) {
        printf("Error: Unable to read flag\n");
        fclose(flag_file);
        return 1;
    }

    fclose(flag_file);

    // 移除可能的换行符
    flag[strcspn(flag, "\n")] = 0;

    // 输出flag
    printf("%s\n", flag);

    return 0;
}
