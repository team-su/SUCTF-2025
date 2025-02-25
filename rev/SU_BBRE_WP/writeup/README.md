chatgpt或者手动将汇编还原为c代码，源码如下：

```
//gcc -m32 -O0 -fno-stack-protector -fno-pie -o test test01.c -Wl,-Ttext-segment=0x401000

#include<stdio.h>
#include<string.h>
#include <stdlib.h>
int function0(char*input);   //test
void function1();            //part2
void function2();            //part1
void function3(unsigned char *key, int keyLength, unsigned char *S);    //keySchedulingAlgorithm
void function4(unsigned char *S, unsigned char *data, int dataLength);    //pseudoRandomGenerationAlgorithm
void function5(unsigned char *key, int keyLength, unsigned char *data, int dataLength);         //rc4
int main()
{
    char input[100];
    printf("please input your flag:");
    scanf("%19s",input);
    function2(input);
    function0(input);
}

void function1()
{
    char input2[10];
    // unsigned char cpdata[9]={0x39,0x51,0x02,0x56,0x2c,0xac,0x0e,0xa9,0xcc};
    char cpdata[9]={0x41,0x6d,0x62,0x4d,0x53,0x49,0x4e,0x29,0x28};
    printf("hhh,you find me:\n");
    scanf("%s",input2);

    for(int i=0;i<9;i++)
    {
        if((input2[i]-i)!=cpdata[i])
        {
            exit(0);
        }
    }
    printf("congratulate!!!\n");
    exit(0);
}

int function0(char*input)
{
    char destination[4];     
    
    strcpy(destination,input);
   
    return 0;
};

void function2(char* input)
{
    unsigned char cpdata[16]={0x2f,0x5a,0x57,0x65,0x14,0x8f,0x69,0xcd,0x93,0x29,0x1a,0x55,0x18,0x40,0xe4,0x5e};
    //flag第一段验证逻辑
    function5("suctf",5,input,16);
    for(int i=0;i<16;i++)
    {
        if((input[i]&0xff)!=cpdata[i])
        {
            //printf("input:%02x cpdata:%02x",input[i]&0xff,cpdata[i]);
            exit(0);
        }
        //printf("%02x",input[i]);
    }
}

// 初始化密钥调度算法
void function3(unsigned char *key, int keyLength, unsigned char *S) {
    int i, j = 0;
    for (i = 0; i < 256; i++) {
        S[i] = i;
    }
    for (i = 0; i < 256; i++) {
        j = (j + S[i] + key[i % keyLength]) % 256;
        unsigned char temp = S[i];
        S[i] = S[j];
        S[j] = temp;
    }
}

// 伪随机生成算法
void function4(unsigned char *S, unsigned char *data, int dataLength) {
    int i = 0, j = 0, k;
    for (int n = 0; n < dataLength; n++) {
        i = (i + 1) % 256;
        j = (j + S[i]) % 256;
        unsigned char temp = S[i];
        S[i] = S[j];
        S[j] = temp;
        k = S[(S[i] + S[j]) % 256];
        data[n] ^= k;
    }
}

// RC4 加密函数
void function5(unsigned char *key, int keyLength, unsigned char *data, int dataLength) {
    unsigned char S[256];
    function3(key, keyLength, S);
    function4(S, data, dataLength);
}




```

由function2处逻辑，解rc4得到第一段flag `We1com3ToReWorld`，正常输入下执行完function0，程序结束，congratulate!!!逻辑在function1处，在看function0处strcpy有溢出问题，根据地址function1的地址40223D，参照ascii表转为相应字符，注意栈中存储小端序。

![](E:\RE\CTF\SU_BBRE_WP\writeup\picture1.png)

实际flag：We1com3ToReWorld="@AndPWNT00