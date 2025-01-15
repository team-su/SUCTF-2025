import torch
import torch.nn as nn
import numpy as np
import random
import math
from tqdm import tqdm

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.linear = nn.Linear(n, n * n)
        self.conv = nn.Conv2d(1, 1, (2, 2), stride=1, padding=1)
        self.conv1 = nn.Conv2d(1, 1, (3, 3), stride=3)

    def forward(self, x):
        x = x.view(1, 1, 3, 3 * n)
        x = self.conv1(x)
        x = x.view(n)
        x = self.linear(x)
        x = x.view(1, 1, n, n)
        x = self.conv(x)
        return x

# 加载模型
for n in range(100):
    try:
        # n = 9 # 假设每个字符用9位表示
        mynet = Net()
        mynet.load_state_dict(torch.load('model.pth'))
        # mynet.eval()
        print(n)
        break
    except:
        continue

# 加载密文
def load_ciphertext(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
        ciphertext = []
        for line in lines:
            row = list(map(float, line.strip().split()))
            ciphertext.append(row)
    return torch.tensor(ciphertext).unsqueeze(0).unsqueeze(0)  # 添加batch和channel维度

def get_flag(guess):
    # 假设guess是经过优化后的张量
    final_guess = guess.detach().numpy()
    
    # 根据阈值将数值转换为二进制位
    binary_str_list = [''.join(['1' if final_guess[j] > 0.5 else '0' for j in range(i, i + 9)]) for i in range(0, len(final_guess), 9)]
    
    # 将二进制字符串转换为字符
    flag = ''.join([chr(int(binary_str, 2)) for binary_str in binary_str_list])
    return flag

def to_data(flag):
    data = ''.join(format(ord(i), '09b') for i in flag)
    return torch.tensor([int(i) for i in data], dtype=torch.float32)

# 加载密文
ciphertext = load_ciphertext('ciphertext.txt')

# 定义损失函数
loss_fn = nn.L1Loss()

# 初始化猜测
n = 48  # 假设 n 已经确定
guess = torch.rand((n * 9,), requires_grad=True)
guess = torch.tensor(guess, dtype=torch.float32)
print(guess.size())

# 贪心算法优化
i = 0
best_loss = math.inf
times = 10000

while True:
    for epoch in range(n * 9):  # 迭代次数可以根据实际情况调整
        loss_list = []
        for j in [i / times for i in range(times + 1)]:
            guess[epoch] = j
            output = mynet(guess)
            loss_list.append(loss_fn(output, ciphertext).item())
        
        x = loss_list.index(min(loss_list))
        guess[epoch] = x / times
        
        if loss_list[x] < best_loss:
            best_loss = loss_list[x]
            print(i, get_flag(guess), best_loss)
            print("good")
        
    i += 1
    print(i, get_flag(guess), best_loss)