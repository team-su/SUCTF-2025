import torch
import torch.nn as nn
import numpy as np
ch=[]
with open('ciphertext.txt', 'r') as file:
    for line in file:
        try:
            line_numbers = line.strip().split()
            ch.append([float(num) for num in line_numbers])
        except ValueError:
            print(f"Ignored non-numeric value(s) in line: {line.strip()}")
print(len(ch))
n=len(ch)-1
class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        self.linear = nn.Linear(n, n*n)
        self.conv=nn.Conv2d(1, 1, (2, 2), stride=1,padding=1)
         # 初始化权重和偏置
        is_invertible = False
        while not is_invertible:
            init_weights = torch.randint(-10, 10, (n*n, n)).float()
            U, S, V = torch.svd(init_weights)
            is_invertible = torch.all(S > 0)
        init_bias = torch.randint(-10, 10, (n*n,)).float()
        self.linear.weight.data = init_weights
        self.linear.bias.data = init_bias

        init_weights = torch.randint(-10, 10, (1,1,2, 2)).float()
        init_bias = torch.randint(-10, 10, (1,)).float()
        self.conv.weight.data = init_weights
        self.conv.bias.data = init_bias

        self.conv1=nn.Conv2d(1, 1, (3, 3), stride=3)
        self.conv1.weight.data =  torch.tensor([[[[1, 2, 4],
                                                [8, 16, 32],
                                                [64, 128, 256]]]], dtype=torch.float32)
        self.conv1.bias.data = torch.randint(-10, 10, (1,)).float()

    def forward(self, x):
        x = x.view(1,1,3, 3*n)
        x = self.conv1(x)
        x = x.view(n)
        x = self.linear(x)
        x = x.view(1, 1, n, n)
        x=self.conv(x)
        return x
mynet=Net()
mynet.load_state_dict(torch.load('model.pth'))
conv_weight=mynet.conv.weight.data.tolist()[0][0]
print(conv_weight)
conv_bias=mynet.conv.bias.tolist()
print(conv_bias)
linear_weight=mynet.linear.weight.data.tolist()
print(len(linear_weight[0]))
linear_bias=mynet.linear.bias.data.tolist()
print(len(linear_bias))
flag=[[0] * n for _ in range(n)]
for i in range(n):
    for j in range(n):
        x=0
        y=0
        z=0
        if i>0:
            y=flag[i-1][j]
            if j>0:
                x=flag[i-1][j-1]
        if j>0:
            z=flag[i][j-1]
        flag[i][j]=ch[i][j]-conv_bias[0]-(conv_weight[0][0]*x+conv_weight[0][1]*y+conv_weight[1][0]*z)
        flag[i][j]/=conv_weight[1][1]
flag=np.array(flag).reshape(n*n)
flag=flag-linear_bias
flag=flag.reshape(n*n,1)
print(flag.shape)
print(np.array(linear_weight).shape)
print(np.linalg.pinv(linear_weight).shape)
flag=np.linalg.pinv(linear_weight)@flag
print(flag)
flag_list = [[0 for _ in range(3*n)] for _ in range(3)]
idx = 0
conv1_bias = round(mynet.conv1.bias.tolist()[0])
for i in flag:
    x = round(i[0]) - conv1_bias
    for j in range(9):
        flag_list[j//3][idx+(j%3)] = x % 2
        x = x // 2
    idx += 3
flag = []
print(flag_list)
for sublist in flag_list:
    flag.extend(sublist)
idx = 0
num = 0
for char in flag:
    num = num*2 + char
    idx += 1
    if idx == 9:
        print(chr(num),end='')
        idx = 0
        num = 0